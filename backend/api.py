import os
from dotenv import load_dotenv
from groq import Groq

import requests
from flask import Flask, request, jsonify

from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app)

client = Groq(
    api_key=os.environ.get("API_KEY"),
)

def get_users():
    url = "https://randomuser.me/api/?results=10" 
    response = requests.get(url, timeout=20) 
    if response.status_code == 200:
        return response.json()  
    else:
        return {"error": f"Failed to fetch users: {response.status_code}"}


def get_response(text):
    """
    Sends a request to the AI model and returns the response.
    :param text: The user's input text
    :return: The response from the AI model
    """
    try:
        system_message = """
        You are a patient speaking with a doctor. You are experiencing health issues such as mild fever, headache, fatigue, or any other common symptoms. 
        Respond to the doctor's questions with honesty, but keep in mind that you are just a patient who may or may not know the full details of their condition.
        Avoid providing medical advice or over-explaining. Just answer based on the common symptoms and your understanding.


        """
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_message}, 
                {"role": "user", "content": text} 
            ],
            model="llama3-8b-8192"
        )
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Sorry, I could not generate a response at the moment."




@app.route("/response", methods=["POST"])
def response():
    try:
        data = request.get_json()
        query = data.get("query")
        response = get_response(query)
        return jsonify({"response": response})
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


def get_users():
    url = "https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=10"
    response = requests.get(url)
    return response.json()


@app.route("/test_users", methods=["GET"])
def test_users():
    try:
        response = get_users()
        users = response["data"]["data"]
        return jsonify(users)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
