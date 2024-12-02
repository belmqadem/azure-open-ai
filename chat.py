import requests
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("GPT_ENDPOINT")
IMAGE_ENDPOINT = os.getenv("IMAGE_ENDPOINT")

headers = {
    "Content-Type": "application/json",
    "api-key": API_KEY,
}

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
        response.raise_for_status()
        return response.json()["choices"][0]["message"][
            "content"
        ]
    except requests.RequestException as e:
        return f"Error: {str(e)}"


# Send a request to Azure DALL-E endpoint to generate an image
def generate_image(prompt):
    payload = {"prompt": prompt, "n": 1, "size": "1024x1024", "model": "dall-e-3"}
    try:
        response = requests.post(IMAGE_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        image_url = response.json()["data"][0]["url"]  # Extract the image URL
        return image_url
    except requests.RequestException as e:
        return f"Error: {str(e)}"


# Gradio Interface for GPT-4
def generate_response(prompt):
    text_response = chat_with_gpt(prompt)
    return text_response


# Gradio Interface for DALL-E
def generate_dalle_image(prompt):
    image_url = generate_image(prompt)
    return image_url


# Gradio interface setup
with gr.Blocks(
    css="""
.gradio-container {
    background-color: #2d3436;
    color: #dfe6e9;
    font-family: 'Arial', sans-serif;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding: 40px;
    box-sizing: border-box;
    height: 100vh;
    overflow-y: auto;
}

.gradio-markdown {
    text-align: center;
    color: #74b9ff;
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 30px;
    width: 100%;
}

.gradio-input, .gradio-textbox {
    background-color: #34495e;
    border: 1px solid #7f8c8d;
    border-radius: 10px;
    color: #dfe6e9;
    font-size: 16px;
    padding: 15px;
    width: 100%;
    max-width: 600px;
    margin-bottom: 15px;
    height: 50px;
    box-sizing: border-box;
}

.gradio-input:focus, .gradio-textbox:focus {
    border-color: #74b9ff;
    outline: none;

.gradio-button {
    background-color: #74b9ff;
    border: none;
    color: white;
    font-size: 18px;
    padding: 15px;
    border-radius: 10px;
    cursor: pointer;
    width: 100%;
    max-width: 600px;
    margin-bottom: 30px;
    transition: background-color 0.3s ease;
}

.gradio-button:hover {
    background-color: #0984e3;
}

.gradio-button:active {
    background-color: #016aa7;
}

.gradio-image {
    width: 100%;
    height: auto;
    border-radius: 10px;
    border: 1px solid #7f8c8d;
    max-width: 600px;
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
    background-color: #0984e3;
}

.gradio-row {
    margin-bottom: 20px;
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
