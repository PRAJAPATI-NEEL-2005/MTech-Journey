"""
================================================================================
Assignment 9: PM2.5 Concentration Prediction & Environmental Data Analysis
Date: 05/11/2026
Objective:
Build and evaluate machine learning models to predict PM2.5 concentrations
using environmental parameters. Perform data analysis, preprocessing, feature
extraction, and dimensionality reduction using Pandas, NumPy, and Scikit-learn.
================================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# ==============================================================================
# 1. Load the Given Dataset
# ==============================================================================
print("=" * 60)
print("1. LOADING THE DATASET")
print("=" * 60)

# Read the provided air quality dataset
df = pd.read_excel('air_quality_data.xlsx')
print("Dataset loaded successfully!")

# ==============================================================================
# 2. Inspect the Data
# ==============================================================================
print("\n" + "=" * 60)
print("2. INSPECTING THE DATA")
print("=" * 60)

# Check data shape
print("\nData Shape:", df.shape)

# Check column names
print("\nColumn Names:", df.columns.tolist())

# DataFrame info
print("\nDataFrame Info:")
df.info()

# Display first 5 and last 5 records
print("\nFirst 5 Records:")
print(df.head())

print("\nLast 5 Records:")
print(df.tail())

# Display number of rows and columns
print(f"\nNumber of Rows: {df.shape[0]}")
print(f"Number of Columns: {df.shape[1]}")

# Check for missing values and duplicate records
print("\nMissing Values Count:")
print(df.isna().sum())

print(f"\nDuplicate Records Count: {df.duplicated().sum()}")

# Generate descriptive statistics
print("\nDescriptive Statistics (describe):")
print(df.describe())

# Display column data types
print("\nData Types:")
print(df.dtypes)

# Convert the Date column into the appropriate datetime format
df['Date'] = pd.to_datetime(df['Date'])
print("\nDate column converted to datetime format successfully.")

# Select any one input feature (Temperature, Humidity, PM10) and consider PM2.5 as output
selected_feature = 'Temperature'
X_single = df[[selected_feature]]
y_target = df['PM2.5']
print(f"\nSelected Single Input Feature: {selected_feature}")
print(f"Target Variable (Dependent): PM2.5")

# ==============================================================================
# 3. Data Analysis Using Pandas and NumPy
# ==============================================================================
print("\n" + "=" * 60)
print("3. DATA ANALYSIS USING PANDAS AND NUMPY")
print("=" * 60)

# Calculate average, maximum, and minimum values of environmental parameters
summary_stats = df[['Temperature', 'Humidity', 'PM2.5', 'PM10']].agg(['mean', 'max', 'min'])
print("\nSummary Statistics (Mean, Max, Min):")
print(summary_stats)

# Group the data by month and calculate average PM2.5
monthly_avg = df.groupby(df['Date'].dt.to_period('M'))['PM2.5'].mean()
print("\nMonthly Average PM2.5:")
print(monthly_avg)

# Filter records where PM2.5 exceeds a student-specified threshold (e.g., 60 µg/m³)
threshold = 60
filtered_records = df[df['PM2.5'] > threshold]
print(f"\nNumber of records where PM2.5 > {threshold} µg/m³: {len(filtered_records)}")

# Sort the dataset based on PM2.5 concentrations (descending order)
df_sorted = df.sort_values(by='PM2.5', ascending=False)
print("\nTop 5 Highest PM2.5 Records (Sorted):")
print(df_sorted[['Date', 'PM2.5', 'PM10', 'Temperature', 'Humidity']].head())

# Create a new column representing the month extracted from Date
df['Month'] = df['Date'].dt.month
print("\nMonth column created from Date:")
print(df[['Date', 'Month', 'PM2.5']].head())

# Convert selected columns into NumPy arrays
temp_array = df['Temperature'].to_numpy()
humidity_array = df['Humidity'].to_numpy()
pm25_array = df['PM2.5'].to_numpy()
pm10_array = df['PM10'].to_numpy()
print("\nConverted columns to NumPy arrays. PM2.5 array shape:", pm25_array.shape)

# Calculate mean, median, standard deviation, maximum, and minimum using NumPy
print("\nNumPy Statistical Calculations for PM2.5:")
print(f"Mean:               {np.mean(pm25_array):.4f}")
print(f"Median:             {np.median(pm25_array):.4f}")
print(f"Standard Deviation: {np.std(pm25_array):.4f}")
print(f"Maximum:            {np.max(pm25_array):.4f}")
print(f"Minimum:            {np.min(pm25_array):.4f}")

# Identify records where PM2.5 is greater than its average
pm25_average = df['PM2.5'].mean()
above_avg_records = df[df['PM2.5'] > pm25_average]
print(f"\nPM2.5 Average: {pm25_average:.4f}")
print(f"Total records where PM2.5 > average: {len(above_avg_records)}")

# Calculate the correlation between selected environmental parameters
correlation_matrix = df[['Temperature', 'Humidity', 'PM2.5', 'PM10']].corr()
print("\nCorrelation Matrix between Environmental Parameters:")
print(correlation_matrix)

# Apply array-based operations to create or modify features
# 1. Convert Temperature to Kelvin
df['Temp_Kelvin'] = temp_array + 273.15
# 2. Binary indicator for high pollution (PM2.5 > 50) using np.where
df['High_Pollution_Flag'] = np.where(pm25_array > 50, 1, 0)
print("\nArray-based features created (Temp_Kelvin, High_Pollution_Flag):")
print(df[['Temperature', 'Temp_Kelvin', 'PM2.5', 'High_Pollution_Flag']].head())

# ==============================================================================
# 4. Pre-process the Data
# ==============================================================================
print("\n" + "=" * 60)
print("4. PRE-PROCESSING THE DATA")
print("=" * 60)

# Handle missing values
print("\nMissing values before handling:\n", df.isna().sum())
df = df.dropna()
print("Missing values after handling:\n", df.isna().sum())

# Check for duplicate records
print(f"\nDuplicate records before dropping: {df.duplicated().sum()}")
df = df.drop_duplicates()
print(f"Duplicate records after dropping: {df.duplicated().sum()}")

# ==============================================================================
# 5. Segmentation and Feature Extraction
# ==============================================================================
print("\n" + "=" * 60)
print("5. SEGMENTATION AND FEATURE EXTRACTION")
print("=" * 60)

# A. Segmentation
# Extract hour from Date column
df['Hour'] = df['Date'].dt.hour

def get_time_interval(hour):
    if 6 <= hour <= 11:
        return 'Morning'
    elif 12 <= hour <= 17:
        return 'Afternoon'
    elif 18 <= hour <= 23:
        return 'Evening'
    else: # 0 <= hour <= 5
        return 'Night'

df['Time_Interval'] = df['Hour'].apply(get_time_interval)

interval_avg_pm25 = df.groupby('Time_Interval')['PM2.5'].mean().reset_index()
interval_avg_pm25.columns = ['Time_Interval', 'Average_PM2.5']
print("\nAverage PM2.5 Concentration by Time Interval:")
print(interval_avg_pm25)

# B. Feature Extraction: Create at least four new features
# 1. Hour (df['Hour'])
# 2. Month (df['Month'])
# 3. Temperature-Humidity Difference
df['Temp_Humidity_Diff'] = df['Temperature'] - df['Humidity']

# 4. PM10-to-PM2.5 Ratio (handling zero values safely)
# Note: PM10_PM2.5_Ratio uses target variable PM2.5. Excluded from predictive features.
df['PM10_PM2.5_Ratio'] = np.where(df['PM2.5'] != 0, df['PM10'] / df['PM2.5'], 0.0)

print("\nExtracted Features Preview:")
print(df[['Date', 'Hour', 'Month', 'Temp_Humidity_Diff', 'PM10_PM2.5_Ratio']].head())

# Separate input features (X) and target variable (y)
feature_cols = ['Temperature', 'Humidity', 'PM10', 'Hour', 'Month', 'Temp_Humidity_Diff']
X = df[feature_cols]
y = df['PM2.5']

print(f"\nFeatures (X) Shape: {X.shape}, Target (y) Shape: {y.shape}")
print("Input features selected:", feature_cols)

# Apply appropriate feature scaling using StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("StandardScaler scaling completed successfully. X_scaled shape:", X_scaled.shape)

# ==============================================================================
# 6. Feature Reduction (PCA)
# ==============================================================================
print("\n" + "=" * 60)
print("6. FEATURE REDUCTION (PCA)")
print("=" * 60)

# Apply PCA and select top 2 features (principal components)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

print("Explained Variance Ratio (Top 2 PCs):", pca.explained_variance_ratio_)
print(f"Total Explained Variance: {np.sum(pca.explained_variance_ratio_):.4f}")

pca_df = pd.DataFrame(X_pca, columns=['Principal_Component_1', 'Principal_Component_2'])
print("\nPrincipal Components Preview:")
print(pca_df.head())

# ==============================================================================
# 7. Data Splitting
# ==============================================================================
print("\n" + "=" * 60)
print("7. DATA SPLITTING (SEQUENTIAL 80/20)")
print("=" * 60)

# Sequentially split dataset into Training (80%) and Testing (20%)
train_size = int(0.80 * len(df))

X_train = X_pca[:train_size]
X_test = X_pca[train_size:]
y_train = y.iloc[:train_size]
y_test = y.iloc[train_size:]

print(f"Total Records:           {len(df)}")
print(f"Training Samples (80%):  {len(X_train)} ({len(X_train)/len(df)*100:.1f}%)")
print(f"Testing Samples (20%):   {len(X_test)} ({len(X_test)/len(df)*100:.1f}%)")

# ==============================================================================
# 8. Model Training
# ==============================================================================
print("\n" + "=" * 60)
print("8. MODEL TRAINING")
print("=" * 60)

# Model 1: Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Model 2: Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

print("Linear Regression trained successfully.")
print("Random Forest Regressor trained successfully.")

# ==============================================================================
# 9. Model Evaluation
# ==============================================================================
print("\n" + "=" * 60)
print("9. MODEL EVALUATION")
print("=" * 60)

# Predictions on testing set
y_pred_lr = lr_model.predict(X_test)
y_pred_rf = rf_model.predict(X_test)

# Metrics for Linear Regression
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
mae_lr = mean_absolute_error(y_test, y_pred_lr)
r2_lr = r2_score(y_test, y_pred_lr)

# Metrics for Random Forest Regressor
rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
mae_rf = mean_absolute_error(y_test, y_pred_rf)
r2_rf = r2_score(y_test, y_pred_rf)

eval_results = pd.DataFrame({
    'Performance Metric': ['Root Mean Square Error (RMSE)', 'Mean Absolute Error (MAE)', 'R² Score'],
    'Linear Regression': [rmse_lr, mae_lr, r2_lr],
    'Random Forest Regressor': [rmse_rf, mae_rf, r2_rf]
})
print("\nModel Evaluation Performance Summary:")
print(eval_results.to_string(index=False))

# ==============================================================================
# 10. Visualization
# ==============================================================================
print("\n" + "=" * 60)
print("10. VISUALIZATION")
print("=" * 60)

# 1. Actual vs. Predicted PM2.5 for both models
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].scatter(y_test, y_pred_lr, alpha=0.35, color='#1f77b4', edgecolors='none', label='Predictions')
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Fit')
axes[0].set_title(f'Linear Regression: Actual vs. Predicted PM2.5\n(RMSE: {rmse_lr:.2f}, R²: {r2_lr:.4f})', fontsize=12)
axes[0].set_xlabel('Actual PM2.5 (µg/m³)', fontsize=11)
axes[0].set_ylabel('Predicted PM2.5 (µg/m³)', fontsize=11)
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.6)

axes[1].scatter(y_test, y_pred_rf, alpha=0.35, color='#2ca02c', edgecolors='none', label='Predictions')
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Fit')
axes[1].set_title(f'Random Forest: Actual vs. Predicted PM2.5\n(RMSE: {rmse_rf:.2f}, R²: {r2_rf:.4f})', fontsize=12)
axes[1].set_xlabel('Actual PM2.5 (µg/m³)', fontsize=11)
axes[1].set_ylabel('Predicted PM2.5 (µg/m³)', fontsize=11)
axes[1].legend()
axes[1].grid(True, linestyle='--', alpha=0.6)

plt.tight_layout()
plt.savefig('actual_vs_predicted.png', dpi=150)
print("Saved: actual_vs_predicted.png")
plt.show()

# 2. Monthly average PM2.5 concentration
monthly_data = df.groupby(df['Date'].dt.to_period('M'))['PM2.5'].mean().reset_index()
monthly_data['Date_Str'] = monthly_data['Date'].astype(str)

plt.figure(figsize=(10, 5))
plt.plot(monthly_data['Date_Str'], monthly_data['PM2.5'], marker='o', color='#ff7f0e', linewidth=2.5, markersize=8)
plt.title('Monthly Average PM2.5 Concentration (2022)', fontsize=14, fontweight='bold')
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average PM2.5 (µg/m³)', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('monthly_avg_pm25.png', dpi=150)
print("Saved: monthly_avg_pm25.png")
plt.show()

# 3. PM2.5 distribution using a histogram
plt.figure(figsize=(9, 5))
sns.histplot(df['PM2.5'], kde=True, bins=30, color='#3470a3', edgecolor='black')
plt.title('PM2.5 Concentration Distribution', fontsize=14, fontweight='bold')
plt.xlabel('PM2.5 (µg/m³)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.axvline(df['PM2.5'].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df["PM2.5"].mean():.2f}')
plt.axvline(df['PM2.5'].median(), color='darkgreen', linestyle=':', linewidth=2, label=f'Median: {df["PM2.5"].median():.2f}')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('pm25_distribution.png', dpi=150)
print("Saved: pm25_distribution.png")
plt.show()

# 4. Correlation heatmap of environmental parameters
plt.figure(figsize=(8, 6))
env_columns = ['Temperature', 'Humidity', 'PM2.5', 'PM10', 'Temp_Humidity_Diff']
sns.heatmap(df[env_columns].corr(), annot=True, cmap='coolwarm', fmt='.3f', linewidths=0.5, vmin=-1, vmax=1)
plt.title('Correlation Heatmap of Environmental Parameters', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('correlation_heatmap.png', dpi=150)
print("Saved: correlation_heatmap.png")
plt.show()

print("\nAssignment 9 execution completed successfully!")

