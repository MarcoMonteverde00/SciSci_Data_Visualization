import pandas as pd
import requests
import time

def query_openalex(name, affiliation=None):
    base_url = "https://api.openalex.org/authors"
    params = {"search": name}
    try:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                return results[0]  # Return the best match
        print("\nNo results found for", name)
        return None
    except Exception as e:
        print(f"Error querying OpenAlex for {name}: {e}")
        return None

def enrich_with_openalex(input_file, output_file):
    df = pd.read_excel(input_file)

    # Adjust column names if needed
    surname_col = 'Surname' if 'Surname' in df.columns else df.columns[4]
    name_col = 'Name' if 'Name' in df.columns else df.columns[5]
    ateneo_col = 'Ateneo' if 'Ateneo' in df.columns else df.columns[7]

    openalex_ids = []
    display_names = []
    orcid = []
    h_index = []
    i10_index = []
    works_counts = []
    cited_by_counts = []
    institution = []

    for idx, row in df.iterrows():
        full_name = f"{row[name_col]} {row[surname_col]}"
        affiliation = f"{row[ateneo_col]}" if pd.notna(row[ateneo_col]) else None

        result = query_openalex(full_name, affiliation)
        if result:
            openalex_ids.append(result.get('id', ''))
            display_names.append(result.get('display_name', ''))
            orcid.append(str(result.get('orcid', '')).split('/')[-1] if result.get('orcid') else '')
            h_index.append(result.get('summary_stats', {}).get('h_index', ''))
            i10_index.append(result.get('summary_stats', {}).get('i10_index', ''))
            works_counts.append(result.get('works_count', ''))
            cited_by_counts.append(result.get('cited_by_count', ''))

            # Try to get institution name
            inst_name = ""
            if "last_known_institution" in result and result["last_known_institution"]:
                inst_name = result["last_known_institution"].get("display_name", "")
            elif "affiliations" in result and result["affiliations"]:
                inst_name = result["affiliations"][0].get("institution", {}).get("display_name", "")
            institution.append(inst_name)
        else:
            openalex_ids.append('')
            display_names.append('')
            orcid.append('')
            h_index.append('')
            i10_index.append('')
            works_counts.append('')
            cited_by_counts.append('')
            institution.append('')

        print(f"Processed {idx + 1}/{len(df)}: {full_name}")
        time.sleep(0.05)  # Avoid rate limits

    # Add enrichment to DataFrame
    df['OpenAlex ID'] = openalex_ids
    df['OpenAlex Name'] = display_names
    df['ORCID'] = orcid
    df['H-Index'] = h_index
    df['I10-Index'] = i10_index
    df['Works Count'] = works_counts
    df['Cited By Count'] = cited_by_counts
    df['Institution (OpenAlex)'] = institution

    # Stats
    total_authors = len(df)
    retrieved_count = sum(1 for oid in openalex_ids if oid.strip() != "")
    retrieval_rate = retrieved_count / total_authors * 100

    print(f"\nRetrieved {retrieved_count}/{total_authors} ({retrieval_rate:.2f}%)")

    # Save data + summary
    with pd.ExcelWriter(output_file) as writer:
        df.to_excel(writer, index=False, sheet_name="Authors Data")
        pd.DataFrame({
            "Metric": ["Total Authors", "Retrieved Authors", "Retrieval Rate (%)"],
            "Value": [total_authors, retrieved_count, retrieval_rate]
        }).to_excel(writer, index=False, sheet_name="Summary")

# Example usage
input_file = "./INFO-01_updated.xlsx"
output_file = "./authors_data/INFO-01_authors_enriched.xlsx"
enrich_with_openalex(input_file, output_file)
