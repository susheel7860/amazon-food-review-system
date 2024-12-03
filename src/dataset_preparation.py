
import sqlite3
import pandas as pd

def connect_to_database(db_path):
  """
  Connect to the SQLite database and return a connection object.
  """
  try:
    conn = sqlite3.connect(db_path)
    return conn
  except Exception as e:
    print(f"Error connecting to database: {e}")
    return None

def process_hashes(file_path):
  """
  Read and process the hashes file.
  """
  try:
    with open(file_path, 'r') as f:
      hashes = f.read().splitlines()
    return hashes
  except Exception as e:
    print(f"Error processing hashes file: {e}")
    return None

def process_reviews(csv_path):
  """
  Read and process the reviews CSV file.
  """
  try:
    reviews = pd.read_csv(csv_path)
    return reviews
  except Exception as e:
    print(f"Error processing reviews file: {e}")
    return None

def filter_and_partition_reviews(conn):
  """
  Filters and partitions reviews from the SQLite database.
  - Filters rows where 'Score' is not equal to 3.
  - Partitions scores into 'positive' or 'negative' categories.
  """
  try:
    reviews_df = pd.read_sql_query("SELECT * FROM Reviews WHERE Score != 3", con=conn)

    # Partition scores
    reviews_df['Score'] = reviews_df['Score'].apply(lambda x: 'negative' if x < 3 else 'positive')

    return reviews_df
  except Exception as e:
    print(f"Error filtering and partitioning reviews: {e}")
    return None

def remove_data_redundancy(dataframe):
  """
  Remove redundant rows from the DataFrame based on specific rules:
  1. Exclude rows with duplicate timestamps for the same person.
  2. Remove completely duplicate rows.
  3. If more than three rows have the same values (except 'Score'), create multiple use entries.
  """
  try:
    # Rule 1: Remove duplicate timestamps for the same person
    if 'Timestamp' in dataframe.columns and 'UserId' in dataframe.columns:
      dataframe = dataframe.drop_duplicates(subset=['UserId', 'Timestamp'])

    # Rule 2: Remove completely duplicate rows
    dataframe = dataframe.drop_duplicates()

    # Rule 3: Handle rows with same values (except 'Score') occurring more than three times
    non_score_cols = [col for col in dataframe.columns if col != 'Score']
    grouped = dataframe.groupby(non_score_cols).filter(lambda x: len(x) > 3)
    if not grouped.empty:
      grouped['Use_Count'] = grouped.groupby(non_score_cols).cumcount() + 1
      dataframe = pd.concat([dataframe, grouped])

    return dataframe.reset_index(drop=True)
  except Exception as e:
    print(f"Error during redundancy removal: {e}")
    return dataframe