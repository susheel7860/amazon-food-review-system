
import json
import os
import pandas as pd

def generate_metadata(db_path, hashes_path, csv_path):
  """
  Generate metadata for the SQLite database, hashes file, and CSV file.
  """
  metadata = {}

  # SQLite metadata
  metadata['sqlite'] = sqlite_metadata(db_path)

  # Hashes file metadata
  metadata['hashes'] = hashes_metadata(hashes_path)

  # CSV file metadata
  metadata['csv'] = csv_metadata(csv_path)

  return metadata

def sqlite_metadata(db_path):
  """
  Generate metadata for an SQLite database.
  """
  import sqlite3

  if not os.path.exists(db_path):
    return {"error": "File not found"}

  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    # Get schema for each table
    table_schemas = {}
    for table in tables:
      cursor.execute(f"PRAGMA table_info({table});")
      schema = cursor.fetchall()
      table_schemas[table] = schema

    conn.close()
    return {"tables": tables, "schemas": table_schemas}
  except Exception as e:
    return {"error": str(e)}

def hashes_metadata(hashes_path):
  """
  Generate metadata for a text file containing hashes.
  """
  if not os.path.exists(hashes_path):
    return {"error": "File not found"}

  try:
    with open(hashes_path, 'r') as f:
      lines = f.readlines()

    return {
      "line_count": len(lines),
      "sample": lines[:5]  # Sample first 5 hashes
    }
  except Exception as e:
    return {"error": str(e)}

def csv_metadata(csv_path):
  """
  Generate metadata for a CSV file.
  """
  if not os.path.exists(csv_path):
    return {"error": "File not found"}

  try:
    reviews = pd.read_csv(csv_path)
    return {
      "columns": list(reviews.columns),
      "row_count": len(reviews),
      "sample": reviews.head().to_dict()  # Sample first 5 rows
    }
  except Exception as e:
    return {"error": str(e)}

def save_metadata(metadata, output_dir, save_json, save_csv):
  """
  Save metadata as JSON and/or CSV in the specified directory.
  """
  os.makedirs(output_dir, exist_ok=True)

  if save_json:
    json_path = os.path.join(output_dir, "metadata.json")
    with open(json_path, "w") as json_file:
      json.dump(metadata, json_file, indent=2)
    print(f"Metadata saved as JSON at {json_path}")

  if save_csv:
    csv_path = os.path.join(output_dir, "metadata.csv")
    csv_rows = []

    # Flatten metadata for CSV format
    for key, value in metadata.items():
      if isinstance(value, dict):
        for subkey, subvalue in value.items():
          csv_rows.append({
            "File Type": key,
            "Attribute": subkey,
            "Value": json.dumps(subvalue) if isinstance(subvalue, (dict, list)) else subvalue
          })
      else:
        csv_rows.append({"File Type": key, "Attribute": "value", "Value": value})

    # Save as CSV
    pd.DataFrame(csv_rows).to_csv(csv_path, index=False)
    print(f"Metadata saved as CSV at {csv_path}")