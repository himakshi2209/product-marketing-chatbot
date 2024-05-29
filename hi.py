# Import necessary libraries
import openai
import streamlit as st
from PIL import Image

# Set GPT API key
openai.api_key = "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"

# Function to generate responses through API calls
def generate_response(prompt):
    completions = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        temperature=0.3,
    )
    message = completions.choices[0].text
    return message

# Function to generate an image based on the given text
def generate_image(text):
    # Use OpenAI Image API to generate an image
    response = openai.Image.create(
        models=["dall-e-3"],
        inputs=text,
    )
    image_url = response.data[0].url
    return image_url

# Streamlit App
st.title("Business Analysis Chatbot")

# Context awareness (storing chat)
if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if "past" not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", key="input")
    return input_text

user_input = get_text()

# GPT Prompt
prompt = f'''
You are a business idea generator, marketing expert and business analyst.
For a business idea generation or analysis query enclosed in <> /
provide the following details in brief (in addition to generating an idea where required):
1. Target market, Market size, growth potential and competition /
2. Industry trends/
3. Risks and their requisite mitigation strategies/
Separate all the parameters.

If the text enclosed in <> is not related to your areas of expertise/
generate "NA" as output.
<{user_input}>
'''

# Generate GPT response
output = generate_response(prompt)

# Generate image based on GPT output
image_url = generate_image(output)

# Store session state
if user_input:
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

# Display GPT output and generated image
st.write("Output: ", output)
st.image(image_url, caption='Generated Marketing Poster', use_column_width=True)
