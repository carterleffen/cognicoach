from flask import Flask, jsonify, request, render_template
from .services.chat_services import create_chat, process_user_input

app = Flask(__name__, template_folder='../templates')

# Sample data for chat history
chat_history = {}


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/chat')
def chat():
  return render_template('chat.html')


@app.route('/v1/chat/create', methods=['POST'])
def create_chat_wrapper():
  # TODO: Implement creating a new chat session
  # Generate a new chat id and return it
  chat = create_chat()
  chat_history[chat.chat_id] = chat
  return jsonify({
    'status': 'success',
    'message': 'Chat session created successfully',
    'chat_id': chat.chat_id
  })


@app.route('/v1/chat/<chat_id>/initiate', methods=['POST'])
def initiate_chat(chat_id):
  # TODO: Implement sending a message to the chatbot coach
  message = request.json['message']
  chat = chat_history[chat_id]
  output = initiate_chat(chat, message)
  return jsonify({
    'status': 'success',
    'message': 'Message sent successfully',
    'chat_id': chat_id,
    'message': output
  })


@app.route('/v1/chat/<chat_id>/send', methods=['POST'])
def send_message(chat_id):
  # TODO: Implement sending a message to the chatbot coach
  message = request.json['message']
  chat = chat_history[chat_id]
  output = process_user_input(chat, message)
  return jsonify({
    'status': 'success',
    'message': 'Message sent successfully',
    'chat_id': chat_id,
    'message': output
  })


@app.route('/v1/chat/<chat_id>/history', methods=['GET'])
def get_chat_history(chat_id):
  # TODO: Implement retrieving the chat history for a specific chat session
  # Dont think we need this anymore since every prediction returns a history
  if chat_id not in chat_history:
    return jsonify({'status': 'error', 'message': 'Invalid chat id'})
  return jsonify({
    'status': 'success',
    'message': 'Chat history retrieved successfully',
    'chat_id': chat_id,
    'history': chat_history[chat_id]
  })
