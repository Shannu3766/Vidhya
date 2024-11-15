from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import os
from groq import Groq

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key

socketio = SocketIO(app)

client = Groq(api_key='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')



def generate_request(user_input):
    text=""
    for word in user_input:
        text+=word+" "
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "Get me a sentence with the following words"
            },
            {
                "role": "user",
                "content": text
            }
        ],
        model="llama3-70b-8192"
    )
    return chat_completion.choices[0].message.content

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')
import random
@app.route('/get_random_words', methods=['GET'])
def get_random_words():
    words_list =     [
    "Hello", "hi", "good morning", "good afternoon", "good evening", "Goodbye",
    "Please", "thank you", "you're welcome", "Excuse me", "Sorry",
    "What's your name?", "My name is…", "Nice to meet you",
    "How are you?", "I'm fine", "I'm good", "I'm okay",
    "Yes", "No", "Maybe", "Of course",
    "Mr.", "Mrs.", "Miss", "Sir", "Madam",
    "Friend", "Stranger", "Neighbor", "Classmate", "Teacher",
    "Boy", "Girl", "Man", "Woman", "Child", "Adult",
    "Apple", "Banana", "Orange", "Grapes", "Mango", "Watermelon", "Pineapple",
    "Carrot", "Potato", "Onion", "Tomato", "Cucumber", "Lettuce", "Spinach",
    "Bread", "Rice", "Pasta", "Noodles", "Pizza", "Sandwich", "Salad",
    "Chicken", "Beef", "Fish", "Lamb", "Pork", "Egg",
    "Milk", "Cheese", "Butter", "Yogurt", "Ice cream",
    "Salt", "Pepper", "Sugar", "Spice", "Sauce", "Oil", "Vinegar",
    "Water", "Juice", "Soda", "Tea", "Coffee",
    "Cake", "Cookie", "Chocolate", "Candy",
    "Breakfast", "Lunch", "Dinner", "Snack", "Dessert",
    "Father", "Mother", "Brother", "Sister", "Son", "Daughter",
    "Grandfather", "Grandmother", "Uncle", "Aunt", "Cousin", "Nephew", "Niece",
    "Husband", "Wife", "Partner", "Friend", "Neighbor",
    "Family", "Relative", "Relationship", "Marriage", "Wedding", "Divorce",
    "Love", "Care", "Respect", "Support", "Help", "Trust", "Friendship",
    "Boyfriend", "Girlfriend", "Fiancé", "Fiancée",
    "Parent", "Child", "Baby", "Toddler", "Teenager", "Adult",
    "Father-in-law", "Mother-in-law", "Brother-in-law", "Sister-in-law",
    "Stepfather", "Stepmother", "Stepson", "Stepdaughter"
    ]
    return jsonify({"words": random.sample(words_list, 10)})


@app.route('/submit_selected_words', methods=['POST'])
def submit_selected_words():
    data = request.json
    selected_words = data.get('selected_words', [])
    print(f"Selected Words: {selected_words}")
    response = generate_request(selected_words)
    print(response)
    return jsonify({"status": "success", "selected_words": [response.split(":")[1]]})

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('user_input')
    # response = generate_request(user_input)
    response=user_input
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
