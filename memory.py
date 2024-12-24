import os

from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Get Groq API key
groq_api_key = os.environ.get("API_KEY")
model = "llama3-8b-8192"
# Initialize Groq Langchain chat object and conversation
client = ChatGroq(groq_api_key=groq_api_key, model_name=model)


def main():
    """
    This function is the main entry point of the application. It sets up the Groq client, the Streamlit interface, and handles the chat interaction.
    """

    print(
        "Hello! I'm your friendly Groq chatbot. I can help answer your questions, provide information, or just chat. I'm also super fast! Let's start our conversation!"
    )

    system_prompt = "You are a friendly conversational chatbot"
    conversational_memory_length = 5

    memory = ConversationBufferWindowMemory(
        k=conversational_memory_length, memory_key="chat_history", return_messages=True
    )

    while True:
        user_question = input("Ask a question: ")

        if user_question:

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
            response = conversation.predict(human_input=user_question)
            print("Chatbot:", response)


if __name__ == "__main__":
    main()
