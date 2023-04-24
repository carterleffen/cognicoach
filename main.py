from chat.app import app
# from flask import Flask

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'Hello from Flask!'
# runllm()

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=81)
  # debug=True)