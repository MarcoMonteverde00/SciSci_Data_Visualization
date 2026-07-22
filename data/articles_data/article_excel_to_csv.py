import pandas as pd

# Convert to CSV
pd.read_excel('INFO-01_articles.xlsx').to_csv('INFO-01_articles.csv', index=False)