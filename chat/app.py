from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from .services.chat_services import create_chat, process_user_input, get_history, initiate_chat, history_exists
import logging

app = Flask(__name__,
            template_folder='../templates',
            static_folder='../static')
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Sample data for chat history
CHATS = {}


def get_chat_from_id(chat_id):
  if chat_id not in CHATS:
    logging.error('Chat does not exist')
    return None
  logging.info('Chat id exists!')
  return CHATS[chat_id]


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/chat')
def chat():
  return render_template('chat.html')


@app.route('/v1/chat/create', methods=['POST'])
def create_chat_wrapper():
  chat = create_chat()
  CHATS[chat.chat_id] = chat
  logging.info('Created chat id', chat.chat_id)
  return jsonify({
    'status': 'success',
    'message': 'Chat session created successfully',
    'chat_id': chat.chat_id
  })


@app.route('/v1/chat/complete', methods=['POST'])
def initiate_chat_wrapper():
  message = request.json['message']
  chat_id = request.json['chat_id']
  chat = get_chat_from_id(chat_id)
  if chat is None:
    return jsonify({'status': 'error', 'message': 'Invalid chat id'})
  if history_exists(chat):
    output = process_user_input(chat, message)
  else:
    output = initiate_chat(chat, message)
  return jsonify({
    'status': 'success',
    'message': 'Message sent successfully',
    'chat_id': chat_id,
    'message': output
  })


@app.route('/v1/chat/<chat_id>/history', methods=['GET'])
def get_chat_history(chat_id):
  chat = get_chat_from_id(chat_id)
  if chat is None:
    return jsonify({'status': 'error', 'message': 'Invalid chat id'})
  history = get_history(chat)
  return jsonify({
    'status': 'success',
    'message': 'Chat history retrieved successfully',
    'chat_id': chat_id,
    'history': history
  })
