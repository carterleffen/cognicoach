import os

import uuid
import requests
from chat.models.chat import Chat

from langchain.chat_models import ChatOpenAI

#template
from langchain.prompts import PromptTemplate

#memory
from langchain.memory import ConversationBufferMemory

#chain
from langchain.chains import ConversationChain


def create_chat():
  """Create a new chat instance with a unique chat ID."""
  chat_id = str(uuid.uuid4())
  memory = ConversationBufferMemory()
  chain = ConversationChain(llm=ChatOpenAI(model_name='gpt-3.5-turbo'),
                            verbose=True,
                            memory=memory)
  chat = Chat('123', chat_id, memory, chain)
  return chat


def process_user_input(chat: Chat, user_input: str):
  """Process user input and return chatbot response."""
  # call llm with user input and save history
  return _continue_chat(chat, user_input)


def history_exists(chat: Chat):
  return chat.memory.load_memory_variables({"history"})['history'] != ''


def get_history(chat: Chat):
  """Process user input and return chatbot response."""
  # call llm with user input and save history
  return chat.memory.load_memory_variables({"history"})


def _get_initial_prompt():
  # load initial prompt
  print(os.getcwd())
  with open('ideation_prompt.txt', 'r') as file:
    initialprompt = file.read().replace('\n', '')
  # initialprompt = requests.get(
  #   "https://raw.githubusercontent.com/carterleffen/chatgpt-prompts/main/ideation.prompt"
  # ).text
  # define LLM
  return initialprompt


def initiate_chat(chat: Chat, human_input: str):
  prompt = PromptTemplate(template=f"""{_get_initial_prompt()}
            {{human_input}}""",
                          input_variables=["human_input"])
  formatted_first_prompt = prompt.format(human_input=human_input)
  return _continue_chat(chat, formatted_first_prompt)


def _continue_chat(chat: Chat, human_input):
  # call llm with user input and save history
  output = chat.chain.predict(input=human_input)
  _save_memory(chat.memory, human_input, output)
  return output


def _save_memory(memory, human_input, ai_response):
  memory.chat_memory.add_user_message(human_input)
  memory.chat_memory.add_ai_message(ai_response)
