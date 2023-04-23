class Chat:

  def __init__(self, user_id, chat_id, memory=None, chain=None):
    self.user_id = user_id
    self.chat_id = chat_id
    self.memory = memory
    self.chain = chain
