# Product Search Engine

## Overview

This application serves as a product search engine and shopping assistant that combines a chatbot interface with image generation and search capabilities. Users can interact with the app to find products using natural language and view suggested images or updates based on the input.

---

## Features

* **Chatbot Interaction** : Provides a conversational interface for product queries.
* **Image Search and Display** : Generates images based on user prompts and displays them in a responsive grid.
* **Real-Time Updates** : Dynamically updates the UI with the latest images and responses from the chatbot.
* **Configurable UI Styles** : Tailored with TailwindCSS and DaisyUI for modern and interactive designs.

---

## Prerequisites

* Python 3.8 or higher
* A virtual environment tool (e.g., `venv`, `conda`)
* `pip` package manager
* NVIDIA GPU with CUDA (optional for faster image generation)

---

## Installation and Setup

### Step 1: Clone the Repository

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1" aria-label="Copy"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>Copy code</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">git clone <repository-url>
cd <repository-folder>
</code></div></div></pre>

### Step 2: Create a Virtual Environment

<pre class="!overflow-visible"><div class="contain-inline-size rounded-md border-[0.5px] border-token-border-medium relative bg-token-sidebar-surface-primary dark:bg-gray-950"><div class="flex items-center text-token-text-secondary px-4 py-2 text-xs font-sans justify-between rounded-t-md h-9 bg-token-sidebar-surface-primary dark:bg-token-main-surface-secondary select-none">bash</div><div class="sticky top-9 md:top-[5.75rem]"><div class="absolute bottom-0 right-2 flex h-9 items-center"><div class="flex items-center rounded bg-token-sidebar-surface-primary px-2 font-sans text-xs text-token-text-secondary dark:bg-token-main-surface-secondary"><span class="" data-state="closed"><button class="flex gap-1 items-center select-none py-1" aria-label="Copy"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="icon-sm"><path fill-rule="evenodd" clip-rule="evenodd" d="M7 5C7 3.34315 8.34315 2 10 2H19C20.6569 2 22 3.34315 22 5V14C22 15.6569 20.6569 17 19 17H17V19C17 20.6569 15.6569 22 14 22H5C3.34315 22 2 20.6569 2 19V10C2 8.34315 3.34315 7 5 7H7V5ZM9 7H14C15.6569 7 17 8.34315 17 10V15H19C19.5523 15 20 14.5523 20 14V5C20 4.44772 19.5523 4 19 4H10C9.44772 4 9 4.44772 9 5V7ZM5 9C4.44772 9 4 9.44772 4 10V19C4 19.5523 4.44772 20 5 20H14C14.5523 20 15 19.5523 15 19V10C15 9.44772 14.5523 9 14 9H5Z" fill="currentColor"></path></svg>Copy code</button></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="!whitespace-pre hljs language-bash">python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
</code></div></div></pre>

### Step 3: Install Dependencies

Ensure you have a `requirements.txt` file. 

---

## Running the Application

### Step 1: Start the Server

Run the following command to launch the app: 

>>  python main.py
>>

### Step 2: Open in Browser

Open your browser and navigate to:

---

## CLIP Embeddings Generation

This app uses the CLIP model for generating embeddings for images and text.

### Step 1: Install CLIP Model Dependencies

Ensure `torch` and `clip` libraries are installed in your environment. If not, install them:

### Step 2: Run the Notebook

1. Run the Generate_embeddings.ipynb with your data to generate embeddings and download CLIP embeddings model
2. Update the path to the CLIP model and other required files in the notebook. Use the `pathlib` library or direct paths based on your system configuration.
3. Execute the notebook to generate embeddings for your dataset.

---

## File Structure

* **`main3.py`** : Main application file.
* **`requirements.txt`** : List of dependencies.
* **`Generate_embeddings.ipynb`** : Notebook for generating embeddings using CLIP.
* **`images/`** : Directory for storing and serving local images.

---

## Troubleshooting

* **Error: ModuleNotFoundError** : Ensure all dependencies in `requirements.txt` are installed.
* **Image Not Displaying** : Verify the `LOCAL_IMAGE_DIR` path and ensure images are stored in the correct format.
* **Chatbot Not Responding** : Check API keys and model configurations in the chatbot initialization code.
