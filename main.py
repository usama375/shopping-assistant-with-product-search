from fasthtml.common import *
from claudette import *
import os, uvicorn
from PIL import Image
# from fastcore.parallel import threaded
from src.chatbot import initialize_chat, \
    process_response, function_declarations, generate_custom


# Simulate LLM response (this can be replaced with actual LLM calls)
def simulate_llm_response():
    """Simulate an LLM response that may or may not trigger an image update."""
    # Example response: "yes" indicates image grid should be updated
    # This could come from an actual LLM model, where the decision to update is based on the model's output
    response = "yes"  # Simulated response; change based on actual LLM logic

    if response == "yes":
        perform_llm_function_call("Update based on LLM response")


# Set up headers including Tailwind CSS and Flexbox grid for styling
hdrs = (
    picolink,
    Script(src="https://cdn.tailwindcss.com"),
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/daisyui@4.11.1/dist/full.min.css"),
    Link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/flexboxgrid/6.3.1/flexboxgrid.min.css", type="text/css"),
    Script(src="https://cdn.tailwindcss.com"),
    Style("""
    .chat-bubble-primary {
        background-color: #d1e7dd; /* Light green for user */
        color: #0f5132; /* Dark green text for user */
        border-radius: 10px;
        padding: 10px;
        max-width: 75%;
    }
    .chat-bubble-secondary {
        background-color: #cff4fc; /* Light blue for assistant */
        color: #055160; /* Dark blue text for assistant */
        border-radius: 10px;
        padding: 10px;
        max-width: 75%;
    }
    .chat-end {
        text-align: right;
        margin-bottom: 10px;
    }
    .chat-start {
        text-align: left;
        margin-bottom: 10px;
    }
    .chat-header {
        font-size: 0.9rem;
        font-weight: bold;
        margin-bottom: 5px;
    }
    """),
)

# Chat message component
def ChatMessage(msg, user):
    """Generate a chat message bubble with user or assistant styles."""
    bubble_class = "chat-bubble-primary" if user else "chat-bubble-secondary"
    chat_class = "chat-end" if user else "chat-start"
    return Div(cls=f"chat {chat_class}")(
        Div("User" if user else "Assistant", cls="chat-header"),
        Div(msg, cls=f"chat-bubble {bubble_class}"),
        Hidden(msg, name="messages"),
    )

# Chat input component
def ChatInput():
    """Input field for user messages in the chat interface."""
    return Input(
        name='msg',
        id='msg-input',
        placeholder="Type a message (or 'exit' to quit)",
        cls="input input-bordered w-full",
        hx_swap_oob='true')

# Initialize FastHTML app
app = FastHTML(hdrs=hdrs)

# Store the latest image grid content
app.state.latest_image_grid = "<div>Initial Image Grid</div>"

# Initialize chat with the chatbot
chat = initialize_chat()

# Configuration for local images
LOCAL_IMAGE_DIR = "images"  # Directory containing images
SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif']  # Allowed image formats
IMAGES_TO_DISPLAY = 6  # Number of images to display at once

@app.post("/generate")
def generate(prompt: str = ""):
    """Handle 'Generate' button click to create a new set of images."""
    try:
        image_grid, clear_input = generate_custom(prompt)
        app.state.latest_image_grid = image_grid
        return image_grid, clear_input
    except Exception as e:
        return Div(f"Error: {str(e)}", cls="text-red-500")

# Serve static images
@app.get("/images/{image_name}")
def serve_image(image_name: str):
    """Serve images from the local directory."""
    return FileResponse(os.path.join(LOCAL_IMAGE_DIR, image_name))

# Chat endpoint
@app.post("/chat")
def handle_chat(msg: str, messages: list[str] = None):
    """Handle chat messages sent by the user."""
    if not messages:
        messages = []

    has_function_call = False
    # Check for exit command
    if msg.strip().lower() in ['quit', 'exit', 'bye']:
        return (
            ChatMessage(msg, True),
            ChatMessage("Thank you for shopping with us! Goodbye!", False),
            ChatInput()
        )

    try:
        # Send message to the chatbot
        response = chat.send_message(
            msg,
            tools=[{
                'function_declarations': function_declarations
            }]
        )
        print(response)
        # Process function calls if any
        has_function_call, function_call_response = process_response(response)
        if has_function_call:
            app.state.latest_image_grid = function_call_response
            print("UI Updated")

        # Prepare response text
        response_text = "Found matching shoes based on your requirements!" if has_function_call else response.text

        return (
            ChatMessage(msg, True),
            ChatMessage(response_text, False),
            ChatInput())
    except Exception as e:
        return (
            ChatMessage(msg, True),
            ChatMessage(f"An error occurred, but let's continue our conversation... Error: {str(e)}", False),
            ChatInput()
        )

# Main page route
@app.get("/")
def index():
    """Render the main application page."""
    # Header section
    header = Div(cls="w-full bg-primary text-white p-4 mb-6 shadow-lg")(
        Div(cls="max-w-7xl mx-auto")(
            H1("Product Search Engine", cls="text-2xl font-bold")
        )
    )

    # Chat interface column
    chat_column = Div(cls="w-1/3 h-[calc(100vh-5rem)] p-6 border-r")(
        Div(cls="bg-white rounded-lg shadow-lg p-4 h-full")(
            H2("Shopping Assistant", cls="mb-4 text-xl font-semibold"),
            Form(
                hx_post="/chat",
                hx_target="#chatlist",
                hx_swap="beforeend",
                cls="h-full flex flex-col"
            )(
                Div(id="chatlist", cls="flex-grow overflow-y-auto mb-4"),
                Div(cls="flex space-x-2")(
                    Group(ChatInput(), Button("Send", cls="btn btn-primary"))
                )
            )
        )
    )
    
    # Image search column
    image_column = Div(cls="w-2/3 h-[calc(100vh-5rem)] p-6")(
        Div(cls="bg-white rounded-lg shadow-lg p-4 h-full")(
            H2("Product Search", cls="mb-4 text-xl font-semibold"),
            Form(
                hx_post="/generate",
                hx_target="#display-list2",
                hx_swap="outerHTML"  # Replaces the entire display list
            )(
                Div(cls="flex space-x-2 mb-4")(
                    Input(
                        id="new-prompt",
                        name="prompt",
                        placeholder="Enter your search query..",
                        cls="input input-bordered flex-grow"
                    ),
                    Button("Generate", cls="btn btn-primary")
                )
            ),
            Div(app.state.latest_image_grid, id='display-list'),
            Script("""
            setInterval(async () => {
                const response = await fetch('/get_latest_images');
                const text = await response.text();
                // Replace the display-list content with the updated grid
                document.getElementById("display-list").outerHTML = text;
            }, 2000); // Poll every 5 seconds
            """),
            Div(app.state.latest_image_grid, id='display-list2'),
        )
    )
    
    # Main content layout
    main_content = Div(cls="flex bg-gray-100")(chat_column, image_column)
    
    return Div(cls="min-h-screen")(header, main_content)

@app.get("/get_latest_images")
def get_latest_images():
    """Fetch the latest image grid."""
    return app.state.latest_image_grid

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=int(os.getenv("PORT", default=5000)))
