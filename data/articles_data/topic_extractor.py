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
author_year_topics = defaultdict(lambda: defaultdict(list))

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

        # collect unique topics for this article
        article_topics = set()
        for topic in topics_long:
            parts = topic.split('|')
            field = None
            subfield = None
            topic = None
            for part in parts:
                part = part.strip()
                if part.startswith('Field:'):
                    field = part.replace('Field:', '').strip()
                if part.startswith('Subfield:'):
                    subfield = part.replace('Subfield:', '').strip()
                if part.startswith('Topic:'):
                    topic = part.replace('Topic:', '').strip()
            if field == 'Computer Science' and subfield and topic:
                article_topics.add(str(subfield) + "---" + str(topic))

        # assign unique topics only once per article
        for author in authors:
            if author in target_authors:
                for element in article_topics:
                    author_year_topics[author][year].append(element)

# Build final compact DataFrame
rows = []
for author, years in author_year_topics.items():
    year_dict = {year: dict(Counter(topics)) for year, topics in years.items()}
    rows.append({'Author': author, 'Yearly_Topics': year_dict})

output_df = pd.DataFrame(rows)
output_df.to_csv('INFO-01_topics.csv', index=False, encoding='utf-8')
print("Saved results to 'INFO-01_topics.csv'")
