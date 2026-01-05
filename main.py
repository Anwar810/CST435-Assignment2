import os
import time
import argparse
import filters
import shutil
from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Update this to point to the PARENT 'images' folder, not just 'donuts'
#    This allows you to process multiple food types (donuts, pizza, etc.)
INPUT_FOLDER = os.path.join(BASE_DIR, 'food-101', 'images') 
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'Output')

def process_single_image(args):
    """
    Worker function. Includes lock for proper synchronization.
    """
    # Unpack the lock along with its file details
    file_path, class_name, lock = args 
    
    try:
        filename = os.path.basename(file_path)
        img = filters.load_image(file_path)
        
        # --- PIPELINE (All 5 Filters) ---
        img_gray = filters.to_grayscale(img)
        img_blur = filters.gaussian_blur(img_gray)
        img_edges = filters.sobel_edge_detection(img_blur)
        img_sharpened = filters.sharpen(img_edges)
        final_img = filters.adjust_brightness(img_sharpened, factor=1.5)
        
        # Create output directory
        class_output_dir = os.path.join(OUTPUT_FOLDER, class_name)
        os.makedirs(class_output_dir, exist_ok=True)
        
        # Save result
        output_path = os.path.join(class_output_dir, f"processed_{filename}")
        filters.save_image(final_img, output_path)
        
        # PRINT SUCCESSFUL IMAGE PROCESSING 
        result_msg = f"Success: {class_name}/{filename}"
        
    except Exception as e:
        result_msg = f"Error {class_name}/{os.path.basename(file_path)}: {str(e)}"

    # --- SYNCHRONIZATION MECHANISM ---
    # We use the lock here to ensure 'print' statements don't overlap 
    # when multiple processes finish at the same time.
    with lock:
        print(result_msg)
        
    return result_msg

def run_multiprocessing(tasks, num_workers):
    print(f"--- Starting Multiprocessing with {num_workers} workers ---")
    #Explicit Chunking
    chunksize = max(1, len(tasks) // (num_workers * 4))
    with multiprocessing.Pool(num_workers) as pool:
        pool.map(process_single_image, tasks, chunksize=chunksize)


def run_concurrent_futures(tasks, num_workers):
    print(f"--- Starting Concurrent.Futures with {num_workers} workers ---")
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # Submit tasks and process as they complete for better memory management
        futures = [executor.submit(process_single_image, t) for t in tasks]
        for future in as_completed(futures):
            future.result() # Ensures exceptions are raised if they occurred

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['multi', 'future'], required=True)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()

    # Decide number of workers based on physical cores (load balancing)
    # Caps the worker amount bounded by machine's CPU physical cores
    physical_cores = max(1, os.cpu_count() // 2)
    num_workers = args.workers

    # --- LOCK INITIALIZATION  ---
    # The Manager handles synchronization across different processes 
    manager = multiprocessing.Manager()
    sync_lock = manager.Lock()

    # --- CLEAR THE OUTPUT FILE AT THE START OF EVERY RUN ---
    
    if os.path.exists(OUTPUT_FOLDER):
        shutil.rmtree(OUTPUT_FOLDER)
    os.makedirs(OUTPUT_FOLDER)
    print(f"Cleaned and prepared: {OUTPUT_FOLDER}")

    # --- UPDATED FILE LOADING FOR MULTIPLE CLASSES ---
    # Approximately 250MB file size (5 x ~50MB each image file size)

    target_classes = ['bibimbap','cup_cakes','donuts','dumplings','edamame']
    
    all_tasks = []
    print(f"Scanning for images in: {target_classes}...")

    for class_name in target_classes:
        class_path = os.path.join(INPUT_FOLDER, class_name)
        if os.path.exists(class_path):
            files = [f for f in os.listdir(class_path) if f.endswith('.jpg')]
            # Updated tuple: includes 'sync_lock'
            for f in files:
                all_tasks.append((os.path.join(class_path, f), class_name, sync_lock))
        else:
            print(f"Warning: Folder not found {class_path}")

    print(f"Found {len(all_tasks)} images.")
    
    # Create base output dir
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    start_time = time.perf_counter()
    
    if args.mode == 'multi':
        run_multiprocessing(all_tasks, num_workers)
    elif args.mode == 'future':
        run_concurrent_futures(all_tasks, num_workers)
        
    end_time = time.perf_counter()
    print(f"Total Time: {end_time - start_time:.4f} seconds")