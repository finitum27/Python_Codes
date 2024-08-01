import logging
import os
from pathlib import Path
import hashlib
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from concurrent.futures import ProcessPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the extensions to delete and save
EXTENSIONS_TO_DELETE = ['.odb', '.op2', '.h3d', '.res', '.stt', '.msg', '.rs~', '.prt', '.com', '.sim', '.stat', '.out', '.SMABulk', '.esav', '.mdl']
EXTENSIONS_TO_SAVE = ['.txt', '.pdf', '.inp', '.ppt', '.pptx', '.doc', '.fem', '.bdf', '.docx']
CHUNK_SIZE = 65536  # 64KB
MAX_WORKERS = 8  # Adjust as per your system's capabilities

def hash_file(file_path, chunk_size=CHUNK_SIZE):
    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
    except Exception as e:
        logging.error(f"Error hashing file {file_path}: {e}")
    return hasher.hexdigest()

def index_files(drive, progress_var=None, total_files=None):
    file_index = {}
    all_files = list(Path(drive).rglob('*'))
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(hash_file, file): file for file in all_files if file.is_file()}
        for future in as_completed(futures):
            file = futures[future]
            try:
                file_index[file] = future.result()
            except Exception as e:
                logging.error(f"Error hashing file {file}: {e}")
            if progress_var and total_files:
                progress_var.set(progress_var.get() + 1 / total_files * 100)
    return file_index

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

def sync_file(slave_file, slave_hash, master_drive, slave_drive, master_index, save_folder):
    results = []
    slave_file_path = Path(slave_file)
    master_file_path = Path(str(slave_file_path).replace(str(slave_drive), str(master_drive), 1))
    save_file_path = Path(save_folder) / slave_file_path.name  # Directly save the file in save_folder

    try:
        if master_file_path in master_index:
            if slave_hash == master_index[master_file_path]:
                slave_mod_time = slave_file_path.stat().st_mtime
                master_mod_time = master_file_path.stat().st_mtime
                results.append(f"Comparing files:\nSlave file: {slave_file_path} (Last modified: {slave_mod_time})\nMaster file: {master_file_path} (Last modified: {master_mod_time})")

                if slave_mod_time > master_mod_time:
                    shutil.copy2(slave_file_path, master_file_path)
                    results.append(f"Copied newer file: {master_file_path}")
                slave_file_path.unlink()
                results.append(f"Deleted duplicate file from slave: {slave_file_path}")
            else:
                master_file_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(slave_file_path, master_file_path)
                results.append(f"Copied file: {master_file_path}")
        else:
            master_file_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(slave_file_path, master_file_path)
            results.append(f"Copied file: {master_file_path}")

        # Save file with specific extensions
        if slave_file_path.suffix in EXTENSIONS_TO_SAVE:
            shutil.copy2(slave_file_path, save_file_path)
            results.append(f"Copied file to save folder: {save_file_path}")

    except Exception as e:
        results.append(f"Error syncing file {slave_file_path}: {e}")

    return results

def sync_drives(master_drive, slave_drive, save_folder, progress_var, status_var):
    if not Path(master_drive).exists():
        raise ValueError(f"Master drive path '{master_drive}' does not exist.")
    if slave_drive and not Path(slave_drive).exists():
        raise ValueError(f"Slave drive path '{slave_drive}' does not exist.")
    if save_folder and not Path(save_folder).exists():
        raise ValueError(f"Save folder path '{save_folder}' does not exist.")

    status_var.set("Deleting files with specified extensions...")
    delete_files_with_extensions(master_drive, EXTENSIONS_TO_DELETE, progress_var, len(list(Path(master_drive).rglob('*'))))
    if slave_drive:
        delete_files_with_extensions(slave_drive, EXTENSIONS_TO_DELETE, progress_var, len(list(Path(slave_drive).rglob('*'))))

    status_var.set("Indexing master drive files...")
    master_index = index_files(master_drive, progress_var, len(list(Path(master_drive).rglob('*'))))
    slave_index = {}
    if slave_drive:
        status_var.set("Indexing slave drive files...")
        slave_index = index_files(slave_drive, progress_var, len(list(Path(slave_drive).rglob('*'))))

    status_var.set("Syncing files...")
    total_files = len(master_index) + len(slave_index)
    files_processed = 0

    # Sync files from master to save folder
    if save_folder:
        for master_file, master_hash in master_index.items():
            if master_file.suffix in EXTENSIONS_TO_SAVE:
                save_file_path = Path(save_folder) / master_file.name  # Directly save the file in save_folder
                shutil.copy2(master_file, save_file_path)

    # Sync files from slave to save folder
    if slave_drive and save_folder:
        for slave_file, slave_hash in slave_index.items():
            if slave_file.suffix in EXTENSIONS_TO_SAVE:
                save_file_path = Path(save_folder) / slave_file.name  # Directly save the file in save_folder
                shutil.copy2(slave_file, save_file_path)

    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(sync_file, slave_file, slave_hash, master_drive, slave_drive, master_index, save_folder)
                for slave_file, slave_hash in slave_index.items()]
        for future in as_completed(futures):
            result = future.result()
            for line in result:
                logging.info(line)
            files_processed += 1
            progress_var.set(files_processed / total_files * 100)

    logging.info("All files synced between slave and master drives.")
    write_to_index(master_drive, master_index)
    status_var.set("All files synced.")

def write_to_index(master_drive, files):
    index_file = Path(master_drive) / 'file_index.csv'
    write_header = not index_file.exists()

    with index_file.open('a', newline='') as csvfile:
        fieldnames = ['File Path', 'File Hash']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        for file_path, file_hash in files.items():
            writer.writerow({'File Path': str(file_path), 'File Hash': file_hash})

def select_directory(entry):
    directory = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, directory)

def start_sync(master_entry, slave_entry, save_entry, progress_var, status_var):
    master_drive = master_entry.get()
    slave_drive = slave_entry.get()
    save_folder = save_entry.get()

    if not master_drive or (not slave_drive and not save_folder):
        messagebox.showerror("Error", "Master drive must be specified, along with either slave drive or save folder.")
        return

    try:
        progress_var.set(0)
        status_var.set("Starting synchronization...")
        sync_drives(master_drive, slave_drive, save_folder, progress_var, status_var)
    except ValueError as e:
        logging.error(f"Error: {e}")
        messagebox.showerror("Error", str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        messagebox.showerror("Error", f"Unexpected error: {e}")

def create_gui():
    root = tk.Tk()
    root.title("Drive Sync Tool")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    master_label = ttk.Label(frame, text="Master Drive:")
    master_label.grid(row=0, column=0, sticky=tk.W, pady=5)
    master_entry = ttk.Entry(frame, width=50)
    master_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
    master_browse_button = ttk.Button(frame, text="Browse", command=lambda: select_directory(master_entry))
    master_browse_button.grid(row=0, column=2, sticky=tk.E, pady=5)

    slave_label = ttk.Label(frame, text="Slave Drive (Optional):")
    slave_label.grid(row=1, column=0, sticky=tk.W, pady=5)
    slave_entry = ttk.Entry(frame, width=50)
    slave_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
    slave_browse_button = ttk.Button(frame, text="Browse", command=lambda: select_directory(slave_entry))
    slave_browse_button.grid(row=1, column=2, sticky=tk.E, pady=5)

    save_label = ttk.Label(frame, text="Save Folder (Optional):")
    save_label.grid(row=2, column=0, sticky=tk.W, pady=5)
    save_entry = ttk.Entry(frame, width=50)
    save_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
    save_browse_button = ttk.Button(frame, text="Browse", command=lambda: select_directory(save_entry))
    save_browse_button.grid(row=2, column=2, sticky=tk.E, pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=400, mode="determinate", variable=progress_var)
    progress_bar.grid(row=3, column=0, columnspan=3, pady=10)

    status_var = tk.StringVar()
    status_label = ttk.Label(frame, textvariable=status_var)
    status_label.grid(row=4, column=0, columnspan=3, pady=10)

    sync_button = ttk.Button(frame, text="Start Sync", command=lambda: start_sync(master_entry, slave_entry, save_entry, progress_var, status_var))
    sync_button.grid(row=5, column=0, columnspan=3, pady=10)

    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
