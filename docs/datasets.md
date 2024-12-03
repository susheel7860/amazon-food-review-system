# Dataset: Amazon Fine Food Reviews

## Kaggle Source
- [Dataset Link](https://www.kaggle.com/datasets/snap/amazon-fine-food-reviews/data)

## Metadata

### Files Overview
The dataset contains the following files:
```bash
├── database.sqlite   # SQLite database containing the reviews
├── hashes.txt        # File with hashes for verification
└── Reviews.csv       # CSV file with reviews data

1 directory, 3 files
```

### Dataset Details
- **Total Reviews:** 568,454  
- **Number of Unique Users:** To be calculated  
- **Number of Unique Products:** To be calculated  
- **Time Span:** October 1999 to October 2012  

### Data Columns
The dataset contains 8 columns:

| Column Name   | Description                                      |
|---------------|--------------------------------------------------|
| `Product uuid`| Unique identifier for the product               |
| `Profile name`| User's profile name                             |
| `User name`   | Unique username of the reviewer                 |
| `Time stamp`  | Unix timestamp of the review                    |
| `Score`       | Rating given by the user (scale: 1 to 5)        |
| `Summary`     | Short summary of the review                     |
| `Brief text`  | Full review text                                |

## Data Processing

Refer to the [Data Processing Guide](dataset_preparation.md) for details on preparing and analyzing this dataset.