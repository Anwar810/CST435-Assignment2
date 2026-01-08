# CST435—Parallel and Cloud Computing Assignment
## 📝 Project Overview
This project implements a high-performance parallel image processing pipeline using the prnned Food-101 dataset, and using Python. The primary objective is to analyse the different parallel programming paradigms and evaluate their scalability, speedup, and efficiency when deployed on a Google Cloud Platform (GCP) environment.

## 🚀 Key Features & Filters
The system utilises a  5-stage filtering pipeline for every image:
1. Grayscale Conversion 🌑: Uses the luminance formula $Y = 0.299R + 0.587G + 0.114B$.
2. Gaussian Blur 🌫️: Applies a $3\times3$ kernel for noise reduction and smoothing.
3. Sobel Edge Detection ⚡: Detects intensity gradients to highlight structural edges.
4. Image Sharpening ✨: Enhances fine details using a Laplacian-based sharpening kernel.
5. Brightness Adjustment 💡: Linearly scales pixel values to enhance visual clarity.

## 🖥️ Deployment & Environment
The implementation tasks was carried out on GCP with the following specifications:

| Component    | Specifications |
| -------- | ------- |
| **Machine Type**  | ```c3-standard-8```   |
| **Processor** | 8 vCPUs (4 physical cores)     |
| **Memory**   | 32 GB RAM   |
| **Operating System**  | Debian GNU/Linux 12 (bookworm)   |
| **Boot Disk** | 20 GB Balanced Persistent Disk   |
| **Region/Zone** | ```asia-southeast-1``` (Singapore)  |

## 🛠️ Installation & Setup
1. **Clone and Navigate This Repository**
```
git clone <your-repo-link>
cd <repo-folder>
```

2. **Download the Food-101 Dataset, Extract All and Place the Extracted Folder Inside the Repository**

[Click Here](https://www.kaggle.com/datasets/dansbecker/food-101)

3. **Install Dependencies**

Required for OpenCV to function correctly on headless Linux servers:
   
```
sudo apt-get update && sudo apt-get install -y libgl1-mesa-glx
```

4. **Install Python Libraries**

```
pip3 install -r requirements.txt
```
_Note: Dependencies include `numpy`, `opencv-python`, and `Pillow` for efficient matrix and image operations._


## ⚙️ Usage & Paradigms

The program supports two parallel paradigms: Multiprocessing (`multi`) and Concurrent Features (`future`).

### Option 1: Multiprocessing (`multi`)
Uses a process pool with **explicit chunking** for "excellent efficiency".

```bash
python3 main.py --mode multi --workers 4 # For 4 Workers
```

### Option 2: Concurrent Features (`future`)
Uses a `process pool` with `as_completed` for optimised memory management.

```bash
python3 main.py --mode future --workers 4 # For 4 Workers
```

## 📊 Performance Analysis & Scalability

#### 📝 Results (`multiprocessing`)
| Workers (P) | Multiprocessing Time (s) | Speedup | Efficiency|
|------------|--------------------------|------------------|---------------------|
| 1 (Serial) | 53.8494                  | 1.00x            | 100.00%             |
| 2          | 31.6719                  | 1.70x            | 85.00%              |
| 4          | 15.3408                  | 3.51x            | 87.70%              |
| 6          | 13.4857                  | 3.99x            | 66.50%              |
| 8          | 12.0871                  | 4.45x            | 55.70%              |
| 12         | 11.8202                  | 4.56x            | 38.00%              |

#### 📝 Results (`future`)
| Workers (P) | Concurrent Time (s) | Speedup (Sfutures) | Efficiency (Efutures) |
|-------------|--------------------|-------------------|------------------------|
| 1 (Serial)  | 58.5947            | 1.00x             | 100.00%               |
| 2           | 32.5499            | 1.80x             | 90.00%                |
| 4           | 20.6880            | 2.83x             | 70.80%                |
| 6           | 15.5471            | 3.77x             | 62.80%                |
| 8           | 16.4968            | 3.55x             | 44.40%                |
| 12          | 17.1753            | 3.41x             | 28.40%                |

## 🔍 Key Insights & Bottlenecks
* Amdahl's Law: Our results confirm that speedup is limited by the sequential fraction ($f$), such as I/O operations and initial file scanning.
* Synchronization: A `multiprocessing.Manager().Lock()` was implemented to ensure "proper synchronisation" of console output, preventing interleaved text from multiple processes.
* Granularity: The system uses coarse-grained parallelism (processing one whole image per task) to ensure a high computation-to-communication ratio.

## 📂 Repository Structure
```text
├── food-101/        # Dataset subsets (not included in the repo)
├── Output/          # Processed images directory
├── main.py          # CLI and Parallel Logic 
├── filters.py       # Filter implementations
├── requirements.txt # Python library dependencies
└── README.md        # Project documentation
```

## 🎥YouTube Demo Link:
[Click Here](https://youtu.be/q1aiSGdztPE?si=Wd58DqU8Nsx0D88C)


