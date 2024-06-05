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
        result_label.config(text="Please select both files")
        return
    
    try:
        df_cell_by_gene = pd.read_csv(cell_by_gene)

        df_cell_metadata = pd.read_csv(cell_metadata)

        merged_df = pd.merge(df_cell_by_gene, df_cell_metadata, left_on='cell', right_on='EntityID')

        gene_fields = [col for col in merged_df.columns[2:] if merged_df[col].dtype == 'int64']

        for gene in gene_fields:
            merged_df[gene + '_normalized'] = merged_df[gene] / merged_df['volume']
        
        new_file_name = os.path.join(os.path.dirname(cell_by_gene), "normalized_" + os.path.basename(cell_by_gene))    
        
        normalized_df = merged_df[['cell'] + [gene + '_normalized' for gene in gene_fields]]

        normalized_df.to_csv(new_file_name, index=False)
        
    except Exception as e:
        result_label.config(text=f"Error: {e}")
        
def download():
    new_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if new_file:
        original_file = os.path.join(os.path.dirname(cell_by_gene_label.cget("text")), "normalized_" + os.path.basename(cell_by_gene_label.cget("text")))
        os.rename(original_file, new_file)
        result_label.config(text=f"New CSV downloaded: {new_file}")
            
root = tk.Tk()
root.title("CSV Normalizer")
            
cell_by_gene_label = tk.Label(root, text="No file selected")
cell_by_gene_label.grid(row=0, column=0, padx=10, pady=5)

cell_by_gene_button = tk.Button(root, text="Select File 1", command=lambda: browse_file(cell_by_gene_label))
cell_by_gene_button.grid(row=0, column=1, padx=10, pady=5)

cell_metadata_label = tk.Label(root, text="No file selected")
cell_metadata_label.grid(row=1, column=0, padx=10, pady=5)

cell_metadata_button = tk.Button(root, text="Select File 2", command=lambda: browse_file(cell_metadata_label))
cell_metadata_button.grid(row=1, column=1, padx=10, pady=5)

normalize_button = tk.Button(root, text="Normalize", command=normalize)
normalize_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

download_button = tk.Button(root, text="Download Normalized Data", command=download)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
        

        
