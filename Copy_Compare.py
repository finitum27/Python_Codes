import os
import shutil
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

MAX_WORKERS = 8

def copy_file(slave_file, slave_drive, master_drive):
    try:
        master_file_path = Path(str(slave_file).replace(str(slave_drive), str(master_drive), 1))
        if not master_file_path.exists():
            master_file_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(slave_file, master_file_path)
            logging.info(f"Copied file: {master_file_path}")
    except Exception as e:
        logging.error(f"Error copying file {slave_file} to {master_file_path}: {e}")

def copy_files_if_not_exist(slave_drive, master_drive, progress_var, status_var):
    try:
        slave_files = list(Path(slave_drive).rglob('*'))
        total_files = len(slave_files)
        files_processed = 0

        with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [executor.submit(copy_file, slave_file, slave_drive, master_drive) for slave_file in slave_files if slave_file.is_file()]
            for future in as_completed(futures):
                future.result()  # to raise any exception that occurred during the copy operation
                files_processed += 1
                progress_var.set(files_processed / total_files * 100)
        
        status_var.set("Copying completed.")
        messagebox.showinfo("Info", "Copying completed.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")

def select_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def start_copy(master_entry, slave_entry, progress_var, status_var):
    master_drive = master_entry.get()
    slave_drive = slave_entry.get()

    if not master_drive or not slave_drive:
        messagebox.showerror("Error", "Both master and slave drives must be specified.")
        return

    try:
        progress_var.set(0)
        status_var.set("Starting copy...")
        copy_files_if_not_exist(slave_drive, master_drive, progress_var, status_var)
    except ValueError as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", str(e))

def create_gui_copy():
    root = tk.Tk()
    root.title("Copy Files If Not Exist")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    master_label = ttk.Label(frame, text="Master Drive:")
    master_label.grid(row=0, column=0, sticky=tk.W, pady=5)
    master_entry = ttk.Entry(frame, width=50)
    master_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
    master_browse_button = ttk.Button(frame, text="Browse", command=lambda: select_directory(master_entry))
    master_browse_button.grid(row=0, column=2, sticky=tk.E, pady=5)

    slave_label = ttk.Label(frame, text="Slave Drive:")
    slave_label.grid(row=1, column=0, sticky=tk.W, pady=5)
    slave_entry = ttk.Entry(frame, width=50)
    slave_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
    slave_browse_button = ttk.Button(frame, text="Browse", command=lambda: select_directory(slave_entry))
    slave_browse_button.grid(row=1, column=2, sticky=tk.E, pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", variable=progress_var)
    progress_bar.grid(row=2, column=0, columnspan=3, pady=10)

    status_var = tk.StringVar()
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.grid(row=3, column=0, columnspan=3, pady=10)

    copy_button = ttk.Button(frame, text="Start Copy", command=lambda: start_copy(master_entry, slave_entry, progress_var, status_var))
    copy_button.grid(row=4, column=0, columnspan=3, pady=10)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui_copy()
