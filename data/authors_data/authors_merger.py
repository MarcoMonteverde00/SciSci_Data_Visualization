import pandas as pd

file1 = './INFO-01_authors_enriched.csv'
file2 = '../articles_data/INFO-01_subfields.csv'
file3 = '../articles_data/INFO-01_fields.csv'
file4 = '../articles_data/INFO-01_topics.csv'

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)
df3 = pd.read_csv(file3)
df4 = pd.read_csv(file4)

# merge with subfields
merged_df = pd.merge(df1, df2, right_on='Author', left_on='OpenAlex Name', how='outer')
merged_df = merged_df.drop(columns=["Author"])

# merge with fields
merged_df = pd.merge(merged_df, df3, right_on='Author', left_on='OpenAlex Name', how='outer')
merged_df = merged_df.drop(columns=["Author"])

# merge with topics
merged_df = pd.merge(merged_df, df4, right_on='Author', left_on='OpenAlex Name', how='outer')
merged_df = merged_df.drop(columns=["Author"])

merged_df.to_csv("INFO-01_authors_complete.csv", index=False)
print("Saved merged authors file to 'INFO-01_authors_complete.csv'")