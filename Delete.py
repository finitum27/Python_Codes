import logging
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the extensions to delete
EXTENSIONS_TO_DELETE = ['.odb', '.op2', '.h3d', '.res', '.stt', '.msg', '.rs~', '.prt', '.com', '.sim', '.stat', '.out', '.SMABulk', '.esav', '.mdl']

def delete_files_with_extensions(folder, extensions, progress_var=None, total_files=None):
    all_files = list(Path(folder).rglob('*'))
    for file in all_files:
        if file.is_file() and any(file.suffix == ext for ext in extensions):
            try:
                file.unlink()
                logging.info(f"Deleted file: {file}")
            except Exception as e:
                logging.error(f"Error deleting file {file}: {e}")
        if progress_var and total_files:
            progress_var.set(progress_var.get() + 1 / total_files * 100)

def select_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def start_delete(delete_entry, progress_var, status_var):
    delete_folder = delete_entry.get()

    if not delete_folder:
        messagebox.showerror("Error", "Please specify a folder to delete files from.")
        return

    try:
        progress_var.set(0)
        status_var.set("Deleting files...")
        delete_files_with_extensions(delete_folder, EXTENSIONS_TO_DELETE, progress_var, len(list(Path(delete_folder).rglob('*'))))
        status_var.set("Deletion complete.")
        messagebox.showinfo("Success", "Files deleted successfully.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")

def create_gui():
    root = tk.Tk()
    root.title("File Deletion Tool")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    delete_label = ttk.Label(frame, text="Folder to Delete Files From:")
    delete_label.grid(row=0, column=0, sticky=tk.W, pady=5)
    delete_entry = ttk.Entry(frame, width=50)
    delete_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
    delete_browse_button = ttk.Button(frame, text="Browse", command=lambda: select_directory(delete_entry))
    delete_browse_button.grid(row=0, column=2, sticky=tk.E, pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", variable=progress_var)
    progress_bar.grid(row=1, column=0, columnspan=3, pady=10)

    status_var = tk.StringVar()
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.grid(row=2, column=0, columnspan=3, pady=10)

    delete_button = ttk.Button(frame, text="Start Deletion", command=lambda: start_delete(delete_entry, progress_var, status_var))
    delete_button.grid(row=3, column=0, columnspan=3, pady=10)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
