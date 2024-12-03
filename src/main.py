import argparse
import os
import pandas as pd

from metadata import generate_metadata, save_metadata
from data_processing import (
  connect_to_database,
  process_hashes,
  process_reviews,
  filter_and_partition_reviews,
  remove_data_redundancy
)

__author__ = "susheel"

def main():
  parser = argparse.ArgumentParser(
    description="Process and analyze data files."
  )
  parser.add_argument("--from_path", required=True,
                      help="Path containing SQLite, hashes.txt, and reviews.csv")
  parser.add_argument("--to_path", required=True,
                      help="Output path for generating metadata")
  parser.add_argument("--save_json", action="store_true",
                      help="Flag to save metadata as JSON")
  parser.add_argument("--save_csv", action="store_true",
                      help="Flag to save metadata as CSV")
  parser.add_argument("--save_filtered", action="store_true",
                      help="Flag to save filtered reviews to CSV")

  args = parser.parse_args()
  db_path = os.path.join(args.from_path, 'database.sqlite')
  hash_path = os.path.join(args.from_path, 'hashes.txt')
  reviews_path = os.path.join(args.from_path, 'reviews.csv')

  # Step 1: Generate metadata
  metadata = generate_metadata(db_path, hash_path, reviews_path)
  save_metadata(metadata, args.to_path, args.save_json, args.save_csv)
  print("Metadata generated.")

  # Step 2: Process the database
  conn = connect_to_database(db_path)
  if conn:
    reviews_df = filter_and_partition_reviews(conn)
    if reviews_df is not None:
      print(f"Filtered and partitioned reviews preview:\n{reviews_df.head()}")

      # Step 3: Remove redundancy
      reviews_df = remove_data_redundancy(reviews_df)
      print(f"Reviews after redundancy removal preview:\n{reviews_df.head()}")

      # Step 4: Save filtered reviews (if enabled)
      if args.save_filtered:
        filtered_data_path = os.path.join(args.to_path, "filtered_reviews.csv")
        reviews_df.to_csv(filtered_data_path, index=False)
        print(f"Filtered reviews saved at {filtered_data_path}")

    conn.close()

  # Step 5: Process hashes
  hashes = process_hashes(hash_path)
  if hashes:
    print(f"Hashes (Sample): {hashes[:5]}")  # Display sample hashes

  # Step 6: Process reviews CSV
  reviews_csv = process_reviews(reviews_path)
  if reviews_csv is not None:
    print(f"Reviews CSV preview:\n{reviews_csv.head()}")

if __name__ == "__main__":
  main()