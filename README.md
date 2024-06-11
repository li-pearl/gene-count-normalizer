# Gene Count CSV Normalizer Tool
## Overview
This is a specialized tool with a simple user-friendly application designed to prepare a large dataset for further analysis. The tool can "normalize" gene counts for each cell in a large MERSCOPE-generated CSV file containing cell by gene data using cell volume data from another large CSV with cell metadata values to account for differences in imaged cell volumes. This tool provides a simple interface for selecting files, performing normalization, and downloading the results. The results are formatted in the same manner as the original cell by gene CSV.

## Features
- File Selection Interface
- Normalization:
  - Normalizes gene count fields to account for differences in imaged cell volumes, preparing the dataset for further data analysis
  - Automatically skips specified columns (e.g., Brain Region ID, Brain Region Name).
  - Renames the gene count fields with a _normalized suffix.
  - Notifies users of any cells in the count file that do not have corresponding volume data.
- Downloading Normalized Data:
  - Download the newly generated CSV file.
  - The new file name is prefixed with normalized_.

## Installation
1. Clone the Repository:
```
git clone https://github.com/li-pearl/gene-count-normalizer.git
cd gene-count-normalizer
```

2. Install Dependencies:
```
pip install pandas
```

3. Run the Tool:
```
python normalizer.py
```

## Usage
Select Files: Choose cell by gene and cell metadata files using the buttons.
Normalize Data: Click the "Create and Download Normalized Data" button to perform the normalization process and download the new CSV.
