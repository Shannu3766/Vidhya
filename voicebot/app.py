from http import client
from flask import Flask, render_template, request, jsonify
import os
from deep_translator import GoogleTranslator
from groq import Groq

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key


# Initialize SocketIO with the app
# socketio = SocketIO(app)

# Initialize Groq client
client = Groq(api_key='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')

# Function to generate a request based on user input
def generate_request(user_input):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content

def generate_response(user_input):
    print(user_input)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": ""
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        model="llama3-70b-8192"
    )
    print(chat_completion.choices[0].message.content,"jjjknkjn")
    return chat_completion.choices[0].message.content

# Route for the home page
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()  # Get data from the frontend
    word = data['word']  # The word to be translated
    target_language = data['language']  # Target language code

    # Translate the word using deep-translator
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translation = translator.translate(word)

        # Return the translated word as a JSON response
        return jsonify({'translated_word': translation})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_translation', methods=['POST'])
def translate_word():
    data = request.get_json()  # Get data from the frontend
    word = data['word']  # The word to be translated
    target_language = data['lang']  # Target language code
    # Generate the meaning of the word using the LLaMA API
    language={"en":"English",
          "ml":"Malayalam",
          "te":"Telugu",
          "kn":"Kannada",
          "ta":"Tamil",
          "hi":"Hindi",}
    try:
        # prompt = f"Define the word '{word}' in the language {language[target_language]} in just 10 words for rural kids understanding no need of further breakdown."
        if language[target_language]=="English":
            prompt=f"Give the meaning of the word {word} in english in single sentence in simple english"
        else:
            prompt = f"Give the meaning of the word {word} in {language[target_language]} in single sentence in simple {language[target_language]}"
        meaning = generate_response(prompt)
        print(meaning)
        # Return the translated word as a JSON response
        return jsonify({'translated_word': meaning})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API route to handle user input and generate a response
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    response = generate_request(user_input)
    response=user_input
    return jsonify({"response": response})

if __name__ == '__main__':
    
    app.run(debug=True)
