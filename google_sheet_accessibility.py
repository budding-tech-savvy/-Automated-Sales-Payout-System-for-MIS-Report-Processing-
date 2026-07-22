# Databricks notebook source
# DBTITLE 1,Install required packages
# MAGIC %pip install gspread google-auth

# COMMAND ----------

from google.oauth2.service_account import Credentials
import gspread
import pandas as pd

# COMMAND ----------

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = Credentials.from_service_account_file(
    "/Volumes/raghu/finance/credentials/credentials.json",
    scopes=SCOPES
)

# COMMAND ----------

client = gspread.authorize(creds)

# COMMAND ----------

spreadsheet = client.open_by_key("1xCRuLCHBhvVNBHfAFu3gtOGQD_OD2m_xdzqGpGvouWE")

# COMMAND ----------

worksheet = spreadsheet.sheet1

# COMMAND ----------

data = worksheet.get_all_records()

# COMMAND ----------

import pandas as pd
df = pd.DataFrame(data)
df.shape

# COMMAND ----------

# Convert columns to proper data types based on schema
import re
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

# Define columns by type according to the schema image
date_cols = ['Invoice Date', 'Due Date', 'Payment Date']
integer_cols = ['Untaxed Amount', 'Fiscal Year', 'Taxes', 'Total Untaxed Amount', 
                'Untaxed Amount (USD)', 'Total Amount (USD)', 'Amount Due (USD)']

# Create a copy to avoid modifying original df
df_typed = df.copy()

# Convert date columns to datetime
for col in date_cols:
    if col in df_typed.columns:
        df_typed[col] = pd.to_datetime(df_typed[col], errors='coerce')

# Convert integer columns to numeric (handle as nullable)
for col in integer_cols:
    if col in df_typed.columns:
        df_typed[col] = pd.to_numeric(df_typed[col], errors='coerce')

# Convert all remaining object columns to string to ensure safe Arrow conversion
for col in df_typed.columns:
    if df_typed[col].dtype == 'object' and col not in date_cols:
        df_typed[col] = df_typed[col].fillna('').astype(str)

# Create Spark DataFrame with proper types
spark_df = spark.createDataFrame(df_typed)

# Clean column names by removing invalid characters
clean_df = spark_df.toDF(*[re.sub(r'[^a-zA-Z0-9_]', '_', col) for col in spark_df.columns])

# Save to table with schema overwrite enabled
clean_df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("raghu.finance.invoice_level")