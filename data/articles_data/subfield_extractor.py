import pandas as pd
import ast
from collections import defaultdict, Counter

# Files
papers_file = 'INFO-01_articles.csv'
authors_file = '../authors_data/INFO-01_authors_enriched.xlsx'

# Load authors
df_authors = pd.read_excel(authors_file)
target_authors = set(df_authors['OpenAlex Name'].tolist())

# Initialize dictionary
author_year_subfields = defaultdict(lambda: defaultdict(list))

# Chunked reading
chunk_size = 50000
reader = pd.read_csv(papers_file, chunksize=chunk_size)

for chunk_idx, chunk in enumerate(reader, start=1):
    print(f"Processing chunk {chunk_idx}...")
    for _, row in chunk.iterrows():
        year = row['Year']
        try:
            authors = ast.literal_eval(row['Authors'])
            topics_long = ast.literal_eval(row['Topics (Long form)'])
        except:
            continue

        # collect unique subfields for this article
        article_subfields = set()
        for topic in topics_long:
            parts = topic.split('|')
            field = None
            subfield = None
            for part in parts:
                part = part.strip()
                if part.startswith('Field:'):
                    field = part.replace('Field:', '').strip()
                if part.startswith('Subfield:'):
                    subfield = part.replace('Subfield:', '').strip()
            if field == 'Computer Science' and subfield:
                article_subfields.add(subfield)

        # assign unique subfields only once per article
        for author in authors:
            if author in target_authors:
                for subfield in article_subfields:
                    author_year_subfields[author][year].append(subfield)

# Build final compact DataFrame
rows = []
for author, years in author_year_subfields.items():
    year_dict = {year: dict(Counter(subfields)) for year, subfields in years.items()}
    rows.append({'Author': author, 'Yearly_Subfields': year_dict})

output_df = pd.DataFrame(rows)
output_df.to_csv('INFO-01_subfields.csv', index=False, encoding='utf-8')
print("Saved results to 'INFO-01_subfields.csv'")
