
#### Libraries Used

1. `pandas`
   - Purpose: Data manipulation and analysis.
   - Key Functions:
     - `read_csv`: Reads CSV files into DataFrames.
     - `to_csv`: Writes DataFrames to CSV files.
     - `drop_duplicates`: Removes duplicate rows from DataFrames.
     - `groupby`: Groups DataFrame rows for aggregation.
     - `apply`: Applies functions to DataFrame columns.

2. `sqlite3`
   - Purpose: Interacting with SQLite databases.
   - Key Functions:
     - `connect`: Establishes a connection to the SQLite database.
     - `cursor`: Creates a cursor object for executing SQL queries.
     - `execute`: Executes SQL statements.
     - `close`: Closes the database connection.

3. `argparse`
   - Purpose: Parsing command-line arguments.
   - Key Functions:
     - `ArgumentParser`: Creates a new argument parser.
     - `add_argument`: Defines how a single command-line argument should be parsed.
     - `parse_args`: Parses the arguments passed to the script.

4. `os`
   - Purpose: Interacting with the operating system.
   - Key Functions:
     - `path.join`: Joins one or more path components.
     - `path.exists`: Checks if a given path exists.
     - `makedirs`: Creates directories recursively.

5. `json`
   - Purpose: Working with JSON data.
   - Key Functions:
     - `dump`: Serializes Python objects to a JSON formatted stream.

#### Important Sub-Libraries and Functions

- `pandas.DataFrame`
  - `drop_duplicates(subset)`: Removes duplicate rows based on specified columns.
  - `groupby(columns)`: Groups DataFrame rows based on specified columns for aggregation.
  - `apply(function)`: Applies a function along an axis of the DataFrame.
  - `to_dict()`: Converts DataFrame to a dictionary.

- `sqlite3`
  - `connect(database)`: Connects to the SQLite database.
  - `cursor()`: Returns a cursor object for executing queries.
  - `execute(query)`: Executes a SQL query.
  - `fetchall()`: Fetches all (remaining) rows of a query result.
  - `close()`: Closes the connection.

- `argparse`
  - `ArgumentParser(description)`: Initializes the argument parser with a description.
  - `add_argument(name, options)`: Adds an argument to the parser.
  - `parse_args()`: Parses the arguments passed to the script.

#### Additional Notes

- Error Handling: The script includes basic error handling to catch and display errors during processing. Ensure that the input files exist and have the correct format to avoid errors.
  
- Data Redundancy Rules:
  1. Duplicate Timestamps: Removes rows where the same user has multiple entries with the same timestamp.
  2. Completely Duplicate Rows: Removes rows that are entirely identical.
  3. Multiple Uses: For rows that occur more than three times with the same values (excluding `Score`), a `Use_Count` column is added to indicate multiple uses.

- Saving Data: Data is kept in memory using pandas DataFrames and is only saved to disk if the corresponding flags (`--save_json`, `--save_csv`, `--save_filtered`) are enabled.


## Final Notes

- Running the Script: Ensure all modules (`metadata.py` and `data_processing.py`) are in the same directory as `main.py` or adjust the import paths accordingly.

- Dependencies: Make sure to install the required libraries using `pip` if they are not already installed.

  ```bash
  pip install pandas
  ```
