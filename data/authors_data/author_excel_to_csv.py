import pandas as pd

# Convert to CSV
pd.read_excel('INFO-01_authors_enriched.xlsx').to_csv('INFO-01_authors_enriched.csv', index=False)