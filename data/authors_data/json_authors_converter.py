import pandas as pd
import ast
import json
import numpy as np

csv_file = "INFO-01_authors_complete.csv"
df = pd.read_csv(csv_file, encoding="utf-8")

# Convert stringified dicts back to real dicts
for col in ["Yearly_Subfields", "Yearly_Fields", "Yearly_Topics"]:
    if df[col].dtype == object:
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else {})

# Replace all NaN values with None in all columns
df = df.replace({np.nan: None})

columns_to_keep = [
    "Cognome", "Nome", "OpenAlex ID", "ORCID", 
    "H-Index", "I10-Index", "Works Count", 
    "Cited By Count", "Institution (OpenAlex)", 
    "Yearly_Subfields", "Yearly_Fields", "Yearly_Topics"
]
filtered_df = df[columns_to_keep]

records = filtered_df.to_dict(orient="records")

# Dump safely with json (no truncation)
with open("authors.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=4, ensure_ascii=False)

print("Authors JSON file created successfully!")
