import pandas as pd
import tkinter as tk
from tkinter import filedialog
import os

def browse_file(label):
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*csv")])
    label.config(text=filename)
    return filename

def normalize():
    cell_by_gene = cell_by_gene_label.cget("text")
    cell_metadata = cell_metadata_label.cget("text")

    if cell_by_gene == "No file selected" or cell_metadata == "No file selected":
        status_label.config(text="Please select both files")
        return

    try:
        df_cell_by_gene = pd.read_csv(cell_by_gene)
        df_cell_metadata = pd.read_csv(cell_metadata)

        print("Cell by Gene contents:")
        print(df_cell_by_gene.head())
        print("Cell Metadata contents:")
        print(df_cell_metadata.head())

        # Rename 'entity ID' column in df_volume to 'cell' if necessary
        if 'EntityID' in df_cell_metadata.columns:
            df_cell_metadata.rename(columns={'EntityID': 'cell'}, inplace=True)
            print("Renamed 'entity ID' to 'cell' in cell metadata.")
        else:
            status_label.config(text="Error: 'entity ID' column not found in the cell metadata file. Check if cell metadata was uploaded")
            return

        # # Ensure 'cell' and 'volume' columns are present in df_volume
        # if 'cell' not in df_cell_metadata.columns or 'volume' not in df_cell_metadata.columns:
        #     result_label.config(text="Error: 'cell' or 'volume' column not found in cell ")
        #     return

        # Create a dictionary for quick lookup of volumes by cell
        volume_by_cell_dict = df_cell_metadata.set_index('cell')['volume'].to_dict()

        # Exclude fields that should not be normalized
        exclude_fields = ['cell', 'Brain Region ID', 'Brain Region Name']

        # Identify gene fields to be normalized, excluding the specified fields
        gene_fields = [col for col in df_cell_by_gene.columns if col not in exclude_fields and pd.api.types.is_integer_dtype(df_cell_by_gene[col])]

        print("Count fields identified for normalization:")
        print(gene_fields)
        
        # Collect cells not found in volume_dict
        missing_cells = []
    
        for field in gene_fields:
            df_cell_by_gene[field + '_normalized'] = df_cell_by_gene.apply(
                lambda row: row[field] / volume_by_cell_dict[row['cell']] if row['cell'] in volume_by_cell_dict else None, axis=1
            )
            missing_cells.extend(df_cell_by_gene.loc[~df_cell_by_gene['cell'].isin(volume_by_cell_dict)].cell.unique())

        if missing_cells:
            missing_cells_message = f"Cells not found in volume data: {', '.join(map(str, set(missing_cells)))}"
            print(missing_cells_message)
            status_label.config(text=missing_cells_message)
        else:
            status_label.config(text="Normalization completed successfully.")

        # # Normalize gene fields
        # for field in gene_fields:
        #     df_cell_by_gene[field + '_normalized'] = df_cell_by_gene.apply(lambda row: row[field] / volume_by_cell_dict[row['cell']] if row['cell'] in volume_by_cell_dict else None, axis=1)

        # Create result DataFrame, excluding the original count fields
        result_df = df_cell_by_gene[exclude_fields + [field + '_normalized' for field in gene_fields]]
        
        print("Normalized DataFrame:")
        print(result_df.head())

        # Create the new file name
        new_file_name = os.path.join(os.path.dirname(cell_by_gene), "normalized_" + os.path.basename(cell_by_gene))

        # Save the new DataFrame to a CSV file
        result_df.to_csv(new_file_name, index=False)

        result_label.config(text=f"New CSV created: {new_file_name}")
        # download_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
    except Exception as e:
        status_label.config(text=f"Error: {e}")
        print(e)


# def normalize():
#     cell_by_gene = cell_by_gene_label.cget("text")
#     cell_metadata = cell_metadata_label.cget("text")
    
#     if cell_by_gene == "No file selected" or cell_metadata == "No file selected":
#         result_label.config(text="Please select both files")
#         return
    
#     try:
#         df_cell_by_gene = pd.read_csv(cell_by_gene)
#         df_cell_metadata = pd.read_csv(cell_metadata)
        
#         print("DataFrame 1 contents:")
#         print(df_cell_by_gene.head())
        
#         print("DataFrame 2 contents:")
#         print(df_cell_metadata.head())
        
#         df_cell_metadata.rename(columns={'EntityID': 'cell'}, inplace=True)

#         merged_df = pd.merge(df_cell_by_gene, df_cell_metadata, on='cell')
#         print("Merged DataFrame contents:")
#         print(merged_df.head())

#         gene_fields = [col for col in df_cell_by_gene.columns[2:] if df_cell_by_gene[col].dtype == 'int64']
#         print(gene_fields)
        
#         print(df_cell_metadata['volume'][0])

#         for gene in gene_fields:
#             df_cell_by_gene[gene + '_normalized'] = df_cell_by_gene[gene] / df_cell_metadata['volume'][gene]
        
#         new_file_name = os.path.join(os.path.dirname(cell_by_gene), "normalized_" + os.path.basename(cell_by_gene))    
        
#         normalized_df = df_cell_by_gene[['cell', 'Brain Region ID', 'Brain Region Name'] + [gene + '_normalized' for gene in gene_fields]]
#         print("Normalized DataFrame contents:")
#         print(normalized_df.head())

#         normalized_df.to_csv(new_file_name, index=False)
        
#         result_label.config(text=f"New CSV created and downloaded: {new_file_name}")
#         download_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        
#     except Exception as e:
#         result_label.config(text=f"Error: {e}")
        
# def download():
#     new_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
#     if new_file:
#         original_file = os.path.join(os.path.dirname(cell_by_gene_label.cget("text")), "normalized_" + os.path.basename(cell_by_gene_label.cget("text")))
#         os.rename(original_file, new_file)
#         status_label.config(text=f"New CSV downloaded: {new_file}")
            
root = tk.Tk()
root.title("Gene Count Normalizer")
            
cell_by_gene_label = tk.Label(root, text="No file selected")
cell_by_gene_label.grid(row=0, column=0, padx=10, pady=5)

cell_by_gene_button = tk.Button(root, text="Select cell by gene file", command=lambda: browse_file(cell_by_gene_label))
cell_by_gene_button.grid(row=0, column=1, padx=10, pady=5)

cell_metadata_label = tk.Label(root, text="No file selected")
cell_metadata_label.grid(row=1, column=0, padx=10, pady=5)

cell_metadata_button = tk.Button(root, text="Select cell metadata file", command=lambda: browse_file(cell_metadata_label))
cell_metadata_button.grid(row=1, column=1, padx=10, pady=5)

normalize_button = tk.Button(root, text="Create and Download Normalized Data", command=normalize)
normalize_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

# download_button = tk.Button(root, text="Download Normalized Data", command=download)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

result_label = tk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()