from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import os
from groq import Groq

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

# Initialize SocketIO with the app
socketio = SocketIO(app)

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

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# API route to handle user input and generate a response
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    # response = generate_request(user_input)
    response=user_input
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
