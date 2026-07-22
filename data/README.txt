RESEARCHERS DATA FROM CERCACINECA UPDATED TO 2 SEPTEMBER 2025

The workflow is the following:

if downloading a new version of the file from CercaCineca (.xls file), open in Excel, go to File > Save As and save as .xlsx format, using the name INFO-01_cercacineca.xlsx

INFO-01_cercacineca.xlsx
  |
  |---> normalizer.py
  |
  V
INFO-01.xlsx
  |
  |---> extractor.py
  |
  V
INFO-01_updated.xlsx
  |
  |---> openalex_downloader.py
  |
  V
INFO-01_authors_enriched.xlsx
  |
  |---> openalex_article_retrieval.ipynb -----> INFO-01_authors_enriched.csv 
  |                                        |
  V                              author_excel_to_csv.py
INFO-01_articles.xlsx

After doing this, we have to process the Subfield data. To do so, enter the articles_data folder and execute excel_to_csv.py in order to obtain the CSV from INFO-01_articles.xlsx. Then, execute subfield_extractor.py to obtain INFO-01_subfields.csv
N.B: the subfields are counted ONLY ONCE even if they appear multiple times in the article due to the way OpenAlex stores topics data. We use CSV format because some data exceed the 32'767 characters per cell limit of Excel. 

Similarly to what happens with subfields, we want to obtain INFO-01_fields.csv an INFO-01_topics.csv. To do so, we execute field_extractor.py and topic_extractor.py, very similar to the previous.

From the folder authors_data, run then authors_merger.py to obtain INFO-01_authors_complete.csv, our final and most important processed file.

After all of that, you can run from the authors_data folder the script json_authors_converter.py, in order to create a JSON file with all the authors data that are used in the visualization.

----------------------------------------------
