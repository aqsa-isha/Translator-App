import gradio as gr
import os
import uuid
import requests
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
key = os.environ['KEY']
endpoint = os.environ['ENDPOINT']
location = os.environ['LOCATION']

# Create translation function
def translate_text(original_text, target_language):
    path = '/translate?api-version=3.0'
    target_language_parameter = '&to=' + target_language
    constructed_url = endpoint + path + target_language_parameter

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': original_text}]
    
    # Make the API call
    translator_request = requests.post(constructed_url, headers=headers, json=body)
    translator_response = translator_request.json()
    
    # Return translated text
    return translator_response[0]['translations'][0]['text']

# Define Gradio Interface
iface = gr.Interface(
    fn=translate_text,
    inputs=[
        gr.Textbox(label="Original Text"),
        gr.Dropdown(["en", "es", "fr", "de"], label="Target Language")
    ],
    outputs="text",
    title="Translator App",
    description="Enter text to be translated and select a target language."
)

if __name__ == "__main__":
    iface.launch()