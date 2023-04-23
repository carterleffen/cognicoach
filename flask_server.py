from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Sample data for chat history
chat_history = {}


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/chat')
def chat():
  return render_template('chat.html')


@app.route('/v1/chat/create', methods=['POST'])
def create_chat():
  # TODO: Implement creating a new chat session
  # Generate a new chat id and return it
  chat_id = '123'
  chat_history[chat_id] = []
  return jsonify({
    'status': 'success',
    'message': 'Chat session created successfully',
    'chat_id': chat_id
  })


@app.route('/v1/chat/<chat_id>/send', methods=['POST'])
def send_message(chat_id):
  # TODO: Implement sending a message to the chatbot coach
  message = request.json['message']
  chat_history[chat_id].append(message)
  return jsonify({
    'status': 'success',
    'message': 'Message sent successfully',
    'chat_id': chat_id,
    'message': message
  })


@app.route('/v1/chat/<chat_id>/history', methods=['GET'])
def get_chat_history(chat_id):
  # TODO: Implement retrieving the chat history for a specific chat session
  if chat_id not in chat_history:
    return jsonify({'status': 'error', 'message': 'Invalid chat id'})
  return jsonify({
    'status': 'success',
    'message': 'Chat history retrieved successfully',
    'chat_id': chat_id,
    'history': chat_history[chat_id]
  })


if __name__ == '__main__':
  app.run(debug=True)
