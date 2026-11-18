import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.impute import SimpleImputer

# ==============================================================================
# STEP 1: LOAD & INSPECT THE RAW DATASET
# ==============================================================================
df_raw = pd.read_csv('dirty_cafe_sales.csv')
print("Raw Dataset Shape:", df_raw.shape)   # (10000, 8)
print(df_raw.info())

# ==============================================================================
# STEP 2: STANDARDIZE INVALID TOKENS ('ERROR', 'UNKNOWN' -> np.nan)
# ==============================================================================
df = df_raw.copy()

# Strip accidental whitespace from string columns
for col in df.select_dtypes(include='object').columns:
    df[col] = df[col].str.strip()

# Replace non-standard error placeholders with NumPy NaN
invalid_tokens = ['ERROR', 'UNKNOWN', '', 'N/A', 'null', 'None']
df.replace(invalid_tokens, np.nan, inplace=True)

# ==============================================================================
# STEP 3: DETECT & REMOVE DUPLICATES
# ==============================================================================
print("Exact Duplicate Rows:", df.duplicated().sum())
print("Duplicate Transaction IDs:", df['Transaction ID'].duplicated().sum())
df.drop_duplicates(subset=['Transaction ID'], keep='first', inplace=True)

# ==============================================================================
# STEP 4: DATA TYPE CONVERSION (NUMERIC & DATETIME PARSING)
# ==============================================================================
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Price Per Unit'] = pd.to_numeric(df['Price Per Unit'], errors='coerce')
df['Total Spent'] = pd.to_numeric(df['Total Spent'], errors='coerce')
df['Transaction Date'] = pd.to_datetime(df['Transaction Date'], errors='coerce')

# ==============================================================================
# STEP 5: DOMAIN-RULE DETERMINISTIC & ALGEBRAIC IMPUTATION
# ==============================================================================
# 5a. Exact cafe menu price mapping
item_to_price = {
    'Coffee': 2.0, 'Tea': 1.5, 'Cookie': 1.0, 'Cake': 3.0,
    'Juice': 3.0, 'Sandwich': 4.0, 'Smoothie': 4.0, 'Salad': 5.0
}
price_to_item = {
    1.0: 'Cookie', 1.5: 'Tea', 2.0: 'Coffee',
    3.0: 'Juice', 4.0: 'Sandwich', 5.0: 'Salad'
}

# Recover missing Price Per Unit from Item or from (Total Spent / Quantity)
mask_price = df['Price Per Unit'].isna() & df['Item'].notna()
df.loc[mask_price, 'Price Per Unit'] = df.loc[mask_price, 'Item'].map(item_to_price)

mask_price_calc = df['Price Per Unit'].isna() & df['Total Spent'].notna() & df['Quantity'].notna()
df.loc[mask_price_calc, 'Price Per Unit'] = (
    df.loc[mask_price_calc, 'Total Spent'] / df.loc[mask_price_calc, 'Quantity']
).round(2)

# Recover missing Item from Price Per Unit
mask_item = df['Item'].isna() & df['Price Per Unit'].isin(price_to_item.keys())
df.loc[mask_item, 'Item'] = df.loc[mask_item, 'Price Per Unit'].map(price_to_item)

# 5b. Algebraic identity: Total Spent = Quantity * Price Per Unit
mask_qty = df['Quantity'].isna() & df['Total Spent'].notna() & df['Price Per Unit'].notna()
df.loc[mask_qty, 'Quantity'] = (
    df.loc[mask_qty, 'Total Spent'] / df.loc[mask_qty, 'Price Per Unit']
).round(0)

mask_tot = df['Total Spent'].isna() & df['Quantity'].notna() & df['Price Per Unit'].notna()
df.loc[mask_tot, 'Total Spent'] = (
    df.loc[mask_tot, 'Quantity'] * df.loc[mask_tot, 'Price Per Unit']
).round(2)

# ==============================================================================
# STEP 6: STATISTICAL & ML IMPUTATION (SCIKIT-LEARN)
# ==============================================================================
# Impute remaining numeric gaps using median strategy
num_imputer = SimpleImputer(strategy='median')
df[['Quantity', 'Price Per Unit']] = num_imputer.fit_transform(df[['Quantity', 'Price Per Unit']])
df['Quantity'] = df['Quantity'].astype(int)

# Impute remaining Item gaps using most_frequent strategy
cat_imputer = SimpleImputer(strategy='most_frequent')
df[['Item']] = cat_imputer.fit_transform(df[['Item']])

# Enforce exact price-item alignment and recalculate Total Spent
df['Price Per Unit'] = df['Item'].map(item_to_price)
df['Total Spent'] = (df['Quantity'] * df['Price Per Unit']).round(2)

# Label high-missingness categorical columns transparently & fill chronological dates
df['Payment Method'] = df['Payment Method'].fillna('Not Specified')
df['Location'] = df['Location'].fillna('Not Specified')
df['Transaction Date'] = df['Transaction Date'].ffill().bfill()

# ==============================================================================
# STEP 7: OUTLIER CHECK (IQR) & EXPORT CLEANED DATASET
# ==============================================================================
Q1 = df['Total Spent'].quantile(0.25)
Q3 = df['Total Spent'].quantile(0.75)
IQR = Q3 - Q1
upper_fence = Q3 + 1.5 * IQR  # $24.00 (269 orders of 5 Salads = $25.00 retained as valid)

assert df.isna().sum().sum() == 0, "Null values remain!"
df.to_csv('cleaned_cafe_sales.csv', index=False)
print("Cleansing complete! Remaining nulls:", df.isna().sum().sum())
