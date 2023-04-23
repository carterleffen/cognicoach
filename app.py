from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
auth = HTTPBasicAuth()


class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(50), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)


class ChatSession(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)
  messages = db.relationship('Message', backref='chat_session', lazy=True)


class Message(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  chat_session_id = db.Column(db.Integer,
                              db.ForeignKey('chat_session.id'),
                              nullable=False)
  message = db.Column(db.String(500), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.utcnow)


@auth.verify_password
def verify_password(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.password == password:
    return user


class UserCreation(Resource):

  def post(self):
    username = request.json['username']
    password = request.json['password']
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return {'message': 'User created successfully'}


class UserLogin(Resource):

  @auth.login_required
  def get(self):
    return {'message': 'Login successful'}


class ChatSessionCreation(Resource):

  @auth.login_required
  def post(self):
    user_id = auth.current_user().id
    chat_session = ChatSession(user_id=user_id)
    db.session.add(chat_session)
    db.session.commit()
    return {'message': 'Chat session created successfully'}


class MessageResource(Resource):

  @auth.login_required
  def post(self, chat_id):
    message = request.json['message']
    message = Message(chat_session_id=chat_id, message=message)
    db.session.add(message)
    db.session.commit()
    return {'message': 'Message sent successfully'}

  @auth.login_required
  def get(self, chat_id):
    messages = Message.query.filter_by(chat_session_id=chat_id).all()
    return [{
      'message': m.message,
      'created_at': m.created_at
    } for m in messages]


api.add_resource(UserCreation, '/v1/account/create')
api.add_resource(UserLogin, '/v1/account/login')
api.add_resource(ChatSessionCreation, '/v1/chat/create')
api.add_resource(MessageResource, '/v1/chat/<int:chat_id>/send',
                 '/v1/chat/<int:chat_id>/history')

if __name__ == '__main__':
  db.create_all()
  app.run()
  app.config['DEBUG'] = True
