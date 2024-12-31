import google.generativeai as genai
import os
from fasthtml.common import *
import google.generativeai as genai
import json
import yaml
import random
from pathlib import Path
from clip_search import perform_search

# Load the configuration file to retrieve API keys and other settings
try:
    with open('config.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
except:
    print("Got an Error While Reading Config")

# Set your API key for Google Generative AI
genai.configure(api_key=config['gemini-api-key'])

# Configuration for handling local images
LOCAL_IMAGE_DIR = "images"  # Directory where local images are stored
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif']  # Allowed image formats
IMAGES_TO_DISPLAY = 6  # Number of images to display at once

# Instructions for the LLM to guide its interaction
instructions_for_llm = """
You are a knowledgeable shoe recommendation assistant. Help the customer find the perfect shoes based on their preferences.

Important Instructions:
1. Ask interactive questions to understand user requirements fully.
2. When you have gathered enough information about user preferences, call the product recommendation function.
3. Keep your responses conversational but focused on gathering relevant information.
4. Once you have clear requirements, summarize them and use the perform_search_wrapper function.
5. Not only summarize the requirements but also add your best recommendation for shoes based on customer requirements, 
   for example, if a person asks for outdoor activity shoes, you can suggest "Winter Hiking Boots" or "High Ankle Boots."

Information to gather:
- Event/Occasion
- Primary use
- Style preferences
- Color preferences
- Gender
- Any specific requirements

Limit your response to 15 words only, and be specific.

When you have sufficient information, call the perform_search_wrapper function with a detailed but concise search query.
Do not mention the function or its calling in your responses to the user.
"""

def get_random_images(count=IMAGES_TO_DISPLAY):
    """
    Get multiple random images from the local directory.

    Parameters:
        count (int): Number of random images to select.

    Returns:
        list: List of paths to the selected images.
    """
    image_files = []
    for ext in SUPPORTED_FORMATS:
        image_files.extend(Path(LOCAL_IMAGE_DIR).glob(f'*{ext}'))
    
    if not image_files:
        raise Exception("No images found in the specified directory")
    
    # Select random unique images
    selected_images = random.sample(image_files, min(count, len(image_files)))
    return [str(img) for img in selected_images]

def create_image_card(image_path, prompt):
    """
    Create a card component for a single image.

    Parameters:
        image_path (str): Path to the image.
        prompt (str): Prompt or description for the image.

    Returns:
        Card or Div: The generated card component.
    """
    if os.path.exists(image_path):
        return Card(
            Img(src=f"/images/{os.path.basename(image_path)}", 
                alt="Local image", 
                cls="w-full h-64 object-cover"),
            Div(P(B("Prompt: "), prompt, cls="text-sm"), cls="p-2"),
        )
    else:
        return Div(f"Image not found: {image_path}", cls="text-red-500")

def create_image_grid(image_paths, prompt):
    """
    Create the complete image grid with a status message.

    Parameters:
        image_paths (list): List of paths to images.
        prompt (str): Search prompt or description.

    Returns:
        Div: A container with the image grid and status message.
    """
    return Div(
        # Status message
        Div(
            P(f"Searching for: {prompt if prompt else 'Random Images'}", 
              cls="text-lg font-semibold mb-4 text-blue-600")
        ),
        # Image grid
        Div(
            *[create_image_card(img_path, prompt if prompt else f"Random {i+1}") 
              for i, img_path in enumerate(image_paths)],
            cls="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
        ),
        id='display-list2'
    )

def generate_custom(prompt):
    """
    Generate a custom image grid based on a search prompt.

    Parameters:
        prompt (str): Text prompt for the search.

    Returns:
        tuple: Image grid and input field components.
    """
    # Get top matching images based on the prompt
    image_paths = perform_search(prompt)  # Call search function
    
    # Create image grid with status message
    image_grid = create_image_grid(image_paths, prompt)
    
    # Clear the input field
    clear_input = Input(
        id="new-prompt",
        name="prompt",
        placeholder="Enter a prompt (or leave empty for random images)",
        cls="input input-bordered flex-grow",
        hx_swap_oob='true'
    )
    return image_grid, clear_input

# Function declaration for Gemini API
function_declarations = [{
    "name": "perform_search_wrapper",
    "description": "Search for shoes based on user requirements. \
        - When creating a parameter for function call, don't add 'search for' or 'find for' in the query.",
    "parameters": {
        "type": "object",
        "properties": {
            "text_query": {
                "type": "string",
                "description": "Comprehensive search query based on user requirements"
            }
        },
        "required": ["text_query"]
    }
}]

def initialize_chat():
    """
    Initialize the chat with the model and set up the initial context.

    Returns:
        Chat: Chat instance with predefined instructions.
    """
    model = genai.GenerativeModel("gemini-pro",
                                generation_config={
                                    "temperature": 0.7,
                                    "top_p": 0.8,
                                    "top_k": 40
                                })
    
    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": [instructions_for_llm]
        },
        {
            "role": "model",
            "parts": ["Hello! I'm your shoe shopping assistant. What type of shoes are you looking for today?"]
        }
    ])
    return chat

def perform_search_wrapper(text_query: str):
    """
    Call this function to look for the desired shoes.

    Args:
        text_query (str): Input text query containing user shoe requirements curated by LLM.

    Returns:
        tuple: Image grid and input field components.
    """
    print("\nSearching for shoes with criteria:", text_query)
    response = generate_custom(text_query)
    return response

def process_response(response):
    """
    Process the model's response and handle function calls.

    Parameters:
        response (Response): Model's response to process.

    Returns:
        tuple: Status and processed response, if applicable.
    """
    try:
        function_call = response.candidates[0].content.parts[0].function_call
        args = function_call.args
        if function_call.name == "perform_search_wrapper":
            # Parse arguments and call the function
            response = perform_search_wrapper(args["text_query"])
            return True, response
    except Exception as e:
        print(f"Error processing response: {str(e)}")
    return False, None
