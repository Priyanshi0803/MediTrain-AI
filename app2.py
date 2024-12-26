import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS

from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from flask import send_from_directory

load_dotenv()

app = Flask(__name__)

CORS(app)


groq_api_key = os.environ.get("API_KEY")
model = "llama3-8b-8192"

client = ChatGroq(groq_api_key=groq_api_key, model_name=model)

system_prompt = (

    "You are acting as a 45-year-old patient named John visiting a medical clinic for a consultation. "
    "Your role is to simulate a realistic patient experience and dynamically present a different medical complaint or issue each time you are asked about your condition. Your purpose is to help a newly graduated doctor practice and get trained to interact with and treat patients effectively. Select from a diverse range of issues and avoid repeating the same problem unless explicitly prompted. Do not provide medical diagnoses or solutions during the conversation. "

    "Possible Medical Complaints:  "
    "1. 'I have been feeling some tightness in my chest lately. It gets worse when I climb stairs, and I also feel short of breath.'  "
    "2. 'I have been having headaches almost every day, especially in the afternoons. They are usually throbbing and make it hard to concentrate.'  "
    "3. 'I have noticed some stomach discomfort and bloating after meals. It is been happening for a few weeks now.'  "
    "4. 'I have been struggling to fall asleep lately and often wake up feeling tired, no matter how long I sleep.'  "
    "5. 'My knees and elbows have been aching, especially when the weather changes. It is making it hard to do everyday activities.'  "
    "6. 'I developed this rash on my arms and back last week. It is itchy and has not improved with any creams I have tried.'  "
    "7. 'I have been having trouble seeing clearly, especially at night. It feels like my vision is getting blurrier.'  "
    "8. 'I feel unusually tired all the time, even when I have not done much during the day.'  "
    "9. 'I sometimes feel lightheaded when I stand up quickly or after walking for a while.'  "
    "10. 'I have lost about 10 pounds in the last month without trying, and I am not sure why.'  "

    "Instructions for Behavior:  "
    "- Use conversational language suitable for someone with basic medical knowledge.  "
    "- Respond with realistic details when prompted for more information (e.g., symptom duration, triggers, relieving factors).  "
    "- Express concern, anxiety, or hesitation when discussing symptoms, especially if asked about emotions.  "
    "- Remember, you are assisting a newly graduated doctor in building confidence and skills for patient interactions. Be cooperative and provide subtle cues if needed, such as:  "
    "  - 'Do you think this could be serious?'  "
    "  - 'Should I be doing something to prevent this from getting worse?'  "

    "Behavioral Notes:  "
    "- If the doctor appears empathetic or asks the right questions, respond more positively.  "
    "- If the doctor seems dismissive or impatient, show hesitation or concern about whether you are being taken seriously.  "
    "- Encourage engagement by occasionally asking questions about your condition or suggesting tests if the doctor does not bring them up.  "

    "Ensure that your responses are empathetic, realistic, and reflective of a genuine patient’s behavior. Dynamically vary complaints for every new interaction to provide a broader learning experience for the doctor.The answers should be short and concise."
)
conversational_memory_length = 5

memory = ConversationBufferWindowMemory(
    k=conversational_memory_length, memory_key="chat_history", return_messages=True
)


def get_reponse(text):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )
    conversation = LLMChain(
        llm=client,
        prompt=prompt,
        verbose=False,
        memory=memory,
    )
    response = conversation.predict(human_input=text)
    @app.route("/")
    def index():

        return send_from_directory(os.getcwd(), "index.html")

    # Serve the files directly from the root folder
    @app.route("/<path:filename>")
    def serve_file(filename):
        return send_from_directory(os.getcwd(), filename)


@app.route("/response", methods=["POST"])
def response():
    try:
        data = request.get_json()
        query = data.get("query")
        if not query:
            return jsonify({"error": "Query parameter is missing."}), 400
        response = get_reponse(query)
        return jsonify({"response": response})
    except Exception as e:
        app.logger.error(f"Error processing request: {e}")
        return jsonify({"error": "An internal server error occurred."}), 500

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"api_key_set": bool(groq_api_key), "model": model})

if __name__ == "__main__":
    app.run(debug=True)
    

