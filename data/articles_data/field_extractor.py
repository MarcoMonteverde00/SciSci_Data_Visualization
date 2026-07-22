import pandas as pd
import ast
from collections import defaultdict, Counter

# Files
papers_file = 'INFO-01_articles.csv'
authors_file = '../authors_data/INFO-01_authors_enriched.xlsx'

# Load authors
df_authors = pd.read_excel(authors_file)
target_authors = set(df_authors['OpenAlex Name'].tolist())

# Initialize dictionary: author -> year -> list of "Subfield---Field"
author_year_subfield_fields = defaultdict(lambda: defaultdict(list))

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

        cs_subfields = set()
        other_fields = set()
        
        # Extract subfields and fields
        for topic in topics_long:
            parts = topic.split('|')
            subfield = None
            field = None
            for part in parts:
                part = part.strip()
                if part.startswith('Subfield:'):
                    subfield = part.replace('Subfield:', '').strip()
                elif part.startswith('Field:'):
                    field = part.replace('Field:', '').strip()
            # Collect CS subfields separately
            if subfield and field == 'Computer Science':
                cs_subfields.add(subfield)
            # Collect other fields
            elif field and field != 'Computer Science':
                other_fields.add(field)

        # Create Subfield---Field pairs for each author
        if cs_subfields and other_fields:
            for author in authors:
                if author in target_authors:
                    for cs_sf in cs_subfields:
                        for f in other_fields:
                            author_year_subfield_fields[author][year].append(f"{cs_sf}---{f}")

# Build final compact DataFrame with counts
rows = []
for author, years in author_year_subfield_fields.items():
    year_dict = {year: dict(Counter(pairs)) for year, pairs in years.items()}
    rows.append({'Author': author, 'Yearly_Fields': year_dict})

output_df = pd.DataFrame(rows)
output_df.to_csv('INFO-01_fields.csv', index=False, encoding='utf-8')
print("Saved results to 'INFO-01_fields.csv'")
