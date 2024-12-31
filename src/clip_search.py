import pandas as pd
import re
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
import torch
from PIL import Image
import PIL
import json
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import ast

# Read path dictionary from the file
# This dictionary contains mappings of product names to their respective image file paths
with open("paths_dict.json", 'r') as file:
    image_paths_dict = json.load(file)

# Reading Vectors Stored
# The CSV file contains precomputed embeddings for images
vectors_df = pd.read_csv('vectors.csv')

# Convert string representation of vectors back to numpy arrays
# Each embedding is stored as a string; it needs to be converted back to a numpy array
vectors_df['image_embed'] = vectors_df['image_embed'].apply(lambda x: np.array(ast.literal_eval(f'[{x}]')))  # Wrap string in brackets

## Loading Embeddings Model

# Initializing the CLIP model

# Check for available hardware and set the appropriate device (CUDA, MPS, or CPU)
device = "cuda" if torch.cuda.is_available() else \
         ("mps" if torch.backends.mps.is_available() else "cpu")

model_id = "openai/clip-vit-base-patch32"  # Pretrained CLIP model identifier

# Path to the model can be specified if loading locally
model_id = r"""Path to model"""

# Initialize the tokenizer, processor, and the CLIP model
tokenizer = CLIPTokenizerFast.from_pretrained(model_id)
processor = CLIPProcessor.from_pretrained(model_id)
model = CLIPModel.from_pretrained(model_id).to(device)

## Utils

def encode_text(prompt):
    """
    Encodes the input text into a feature embedding using the CLIP model.

    Parameters:
        prompt (str): Input text prompt.

    Returns:
        torch.Tensor: Text embedding vector.
    """
    # Create transformer-readable tokens
    inputs = tokenizer(prompt, return_tensors="pt")  # pt: Returns PyTorch tensors

    # Use CLIP to encode tokens into a meaningful embedding
    text_emb = model.get_text_features(**inputs)

    return text_emb


def get_image_embd(path):
    """
    Encodes an image into a feature embedding using the CLIP model.

    Parameters:
        path (str): Path to the image file.

    Returns:
        torch.Tensor: Image embedding vector.
    """
    # Open the image file using PIL
    image = Image.open(path)
    
    # Preprocess the image to make it suitable for the CLIP model
    image = processor(
        text=None,
        images=image,
        return_tensors='pt'
    )['pixel_values'].to(device)
    
    # Use CLIP to generate image features
    img_emb = model.get_image_features(image)

    return img_emb


def top_k_cosine_similarity(df, input_vector, k):
    """
    Calculate cosine similarity with all vectors in the DataFrame and return the top k matches.

    Parameters:
        df (pd.DataFrame): DataFrame containing product names and image embeddings.
                           Schema: ['product_name', 'image_embed']
        input_vector (list or np.array): Input vector for comparison.
        k (int): Number of top matches to return.

    Returns:
        pd.DataFrame: DataFrame containing top k matching products with their similarity scores.
    """
    # Convert input_vector to a 2D array (required for cosine_similarity)
    input_vector = np.array(input_vector).reshape(1, -1)
    
    # Convert all image embeddings to a 2D numpy array
    embeddings = np.vstack(df['image_embed'].values)
    
    # Compute cosine similarities
    similarities = cosine_similarity(input_vector, embeddings).flatten()
    
    # Add similarity scores to the DataFrame
    df['similarity'] = similarities
    
    # Get the top k matches based on similarity scores
    top_k_matches = df.nlargest(k, 'similarity')
    
    # Drop the similarity column to keep the DataFrame clean (optional)
    return top_k_matches[['product_name', 'similarity']]


def perform_search(input_text):
    """
    Perform a search for the most similar images based on the input text.

    Parameters:
        input_text (str): The text query to search.

    Returns:
        list: List of file paths for the top matching images.
    """
    # Encode the input text to get its feature embedding
    text_querry = encode_text(prompt=input_text).detach().numpy()[0]
    
    # Find the top 6 most similar images
    results = top_k_cosine_similarity(df=vectors_df, input_vector=text_querry, k=6)
    
    # Map product names to their respective image file paths
    file_paths = [image_paths_dict[file_name] for file_name in results['product_name'].values] 
    
    return file_paths
