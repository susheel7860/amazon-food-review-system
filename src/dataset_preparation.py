import argparse
import os
import pandas as pd
import sqlite3

from .generate_metadata import generate_metadata, save_metadata

__author__ = "susheel"


def process_database(db_path):
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


def filter_and_partition_reviews(db_path):
  """
  Filters and partitions reviews from the SQLite database.
  """
  conn = process_database(db_path)
  if conn is None:
    print("Database connection failed.")
    return None

  try:
    # Fetch reviews where Score is not 3
    filtered_data = pd.read_sql_query(
        "SELECT * FROM Reviews WHERE Score != 3", con=conn)

    # Partition the scores into positive/negative
    def partition(x):
      return 'negative' if x < 3 else 'positive'

    filtered_data['Score'] = filtered_data['Score'].map(partition)
    print(f"Filtered data shape: {filtered_data.shape}")
    print(f"Filtered data preview:\n{filtered_data.head()}")

    return filtered_data
  except Exception as e:
    print(f"Error filtering and partitioning reviews: {e}")
    return None
  finally:
    conn.close()


def main():
  parser = argparse.ArgumentParser(
      description="Process and analyze data files.")
  parser.add_argument("--from_path", required=True,
                      help="Path containing SQLite, hashes.txt, and reviews.csv")
  parser.add_argument("--to_path", required=True,
                      help="Output path for generating metadata")
  parser.add_argument("--save_json", action="store_true",
                      help="Flag to save metadata as JSON")

  args = parser.parse_args()
  db_path = os.path.join(args.from_path, 'database.sqlite')
  hash_path = os.path.join(args.from_path, 'hashes.txt')
  reviews_path = os.path.join(args.from_path, 'reviews.csv')

  # Generate and save metadata
  metadata = generate_metadata(db_path, hash_path, reviews_path)
  save_metadata(metadata, args.to_path, args.save_json)

  # Print metadata
  for key, value in metadata.items():
    print(f"{key.upper()}:\n{value}\n")

  # Process database and export filtered reviews
  filtered_data = filter_and_partition_reviews(db_path)
  if filtered_data is not None:
    filtered_data_path = os.path.join(args.to_path, "filtered_reviews.csv")
    filtered_data.to_csv(filtered_data_path, index=False)
    print(f"Filtered reviews saved at {filtered_data_path}")

  # Process hashes
  hashes = process_hashes(hash_path)
  print(f"Hashes (Sample): {hashes[:5]}")  # Display a sample of hashes

  # Process reviews
  reviews = process_reviews(reviews_path)
  print(f"Reviews preview:\n{reviews.head()}")


if __name__ == "__main__":
  main()
