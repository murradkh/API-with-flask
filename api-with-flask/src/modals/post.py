import uuid
import datetime
from src.modals.database import Database

class Post(object):
    def __init__(self, title, content, author, blog_id,date=datetime.datetime.utcnow(), _id=None):
        self.title = title
        self.content = content
        self.author = author
        self.blog_id = blog_id
        self.date = date
        if _id is None:
            self._id = uuid.uuid4().hex
        else:
            self._id = _id

    def save_to_mong(self):
        Database.insert("posts", self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'date': self.date
        }
    @staticmethod
    def get_from_mongo(_id):
     post_data=Database.find_one("posts", {"_id": _id})
     if post_data is not None:
      return Post(post_data['title'], post_data['content'], post_data['author'], post_data['blog_id'], post_data['date'])
     else:
      return
    @staticmethod
    def get_from_blog(_id):
     return Database.find("posts", {"blog_id": _id})
