import requests
import gradio as gr
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Azure API key for GPT-4
API_KEY = os.getenv("API_KEY")
# Azure API endpoint for GPT-4
ENDPOINT = os.getenv("GPT_ENDPOINT")
# Azure API endpoint for DALL-E
IMAGE_ENDPOINT = os.getenv("IMAGE_ENDPOINT")

# Headers for the request
headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}


# Function to send a request to Azure GPT-4 endpoint
def chat_with_gpt(prompt):
    payload = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800,
    }
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an error for unsuccessful status codes
        return response.json()["choices"][0]["message"][
            "content"
        ]  # Return the GPT response
    except requests.RequestException as e:
        return f"Error: {str(e)}"


# Function to send a request to Azure DALL-E endpoint to generate an image
def generate_image(prompt):
    payload = {"prompt": prompt, "n": 1, "size": "1024x1024", "model": "dall-e-3"}
    try:
        response = requests.post(IMAGE_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an error for unsuccessful status codes
        image_url = response.json()["data"][0]["url"]  # Extract the image URL
        return image_url  # Return the image URL
    except requests.RequestException as e:
        return f"Error: {str(e)}"


# Gradio Interface for GPT-4
def generate_response(prompt):
    text_response = chat_with_gpt(prompt)  # Get GPT-4 response
    return text_response


# Gradio Interface for DALL-E
def generate_dalle_image(prompt):
    image_url = generate_image(prompt)  # Generate image from prompt
    return image_url


# Gradio interface setup
with gr.Blocks(
    css="""
.gradio-container {
    background-color: #2d3436;  /* Dark background for better contrast */
    color: #dfe6e9;  /* Light text for readability */
    font-family: 'Arial', sans-serif;  /* Clean sans-serif font */
    display: flex;
    flex-direction: column;
    justify-content: flex-start;  /* Start alignment for top-down flow */
    align-items: center;
    padding: 40px;
    box-sizing: border-box;
    height: 100vh;  /* Full screen height */
    overflow-y: auto;  /* Enable scrolling if content exceeds screen height */
}

.gradio-markdown {
    text-align: center;
    color: #74b9ff;  /* Light blue for headings */
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 30px;  /* Spacing between title and content */
    width: 100%;
}

.gradio-input, .gradio-textbox {
    background-color: #34495e;  /* Darker input background for contrast */
    border: 1px solid #7f8c8d;  /* Soft border for inputs */
    border-radius: 10px;
    color: #dfe6e9;  /* Light text in input */
    font-size: 16px;
    padding: 15px;
    width: 100%;
    max-width: 600px;  /* Limit input width */
    margin-bottom: 15px;  /* Space between input and button */
    height: 50px;  /* Taller input box for easier typing */
    box-sizing: border-box;  /* Include padding and border in width calculation */
}

.gradio-input:focus, .gradio-textbox:focus {
    border-color: #74b9ff;  /* Blue border when focused */
    outline: none;  /* Remove default focus outline */
}

.gradio-button {
    background-color: #74b9ff;  /* Soft blue background */
    border: none;
    color: white;
    font-size: 18px;
    padding: 15px;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    max-width: 600px;  /* Match button width to input */
    margin-bottom: 30px;  /* Space below the button */
    transition: background-color 0.3s ease;  /* Smooth color transition on hover */
}

.gradio-button:hover {
    background-color: #0984e3;  /* Slightly darker blue on hover */
}

.gradio-button:active {
    background-color: #016aa7;  /* Even darker blue when pressed */
}

.gradio-image {
    width: 100%;
    height: auto;
    border-radius: 10px;
    border: 1px solid #7f8c8d;
    max-width: 600px;  /* Restrict image size */
    margin-top: 20px;
}

.gradio-tab {
    background-color: #74b9ff;
    color: white;
    border-radius: 8px;
    padding: 12px;
    font-weight: bold;
    margin: 10px;
}

.gradio-tab.selected {
    background-color: #0984e3;  /* Darker blue for selected tab */
}

.gradio-row {
    margin-bottom: 20px;  /* Add space between rows */
}
"""
) as demo:
    gr.Markdown("# Azure GPT-4 and DALL-E 3")
    gr.Markdown(
        "Enter a prompt to interact with either GPT-4 for text responses or DALL-E for image generation."
    )

    # Section for GPT-4 Text Generation
    with gr.Tab("GPT-4 Text Generation"):
        with gr.Row():
            prompt_gpt = gr.Textbox(
                label="Enter your prompt", placeholder="e.g., Tell me a joke!", lines=2
            )
            generate_button_gpt = gr.Button("Generate Text Response")
        with gr.Row():
            output_message = gr.Textbox(label="GPT-4 Response", interactive=False)
        generate_button_gpt.click(
            generate_response, inputs=prompt_gpt, outputs=output_message
        )

    # Section for DALL-E Image Generation
    with gr.Tab("DALL-E Image Generation"):
        with gr.Row():
            prompt_dalle = gr.Textbox(
                label="Enter your image prompt",
                placeholder="e.g., A futuristic city skyline at sunset.",
                lines=2,
            )
            generate_button_dalle = gr.Button("Generate Image")
        with gr.Row():
            output_image = gr.Image(
                label="Generated Image", type="filepath", elem_id="image-output"
            )
        generate_button_dalle.click(
            generate_dalle_image, inputs=prompt_dalle, outputs=output_image
        )

# Launch the interface
if __name__ == "__main__":
    demo.launch()
