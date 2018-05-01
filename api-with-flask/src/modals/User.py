import datetime
import uuid

from flask import session

from src.modals.Blog import Blog
from src.modals.database import Database


class User(object):

    def __init__(self,email,password,_id=None):
        self.email=email
        self.password=password
        if _id is None:
            self._id=uuid.uuid4().hex
        else:
            self._id=_id

    @classmethod
    def get_by_email(cls,email):
        data=Database.find_one("users",{"email":email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls,_id):
       data=Database.find_one("users",{"_id":_id})
       if data is not None:
            return cls(**data)

    @classmethod
    def login_valid(cls,email,password):
        user=User.get_by_email(email)
        if user is not None:
            return user.password==password
        return False

    @classmethod
    def register(cls,email,password):
        user = cls.get_by_email(email)
        if user is None:
            new_user= cls(email,password)
            new_user.save_to_mongo()
            session['email']=email
            return True
        else:
            return False
    @staticmethod
    def login(email):
        session['email'] = email
    @staticmethod
    def logout():
        session['email']= None
    def json(self):
        return {
            "email":self.email,
            "_id":self._id,
            "password":self.password
        }
    def save_to_mongo(self):
        Database.insert("users",self.json())

    def get_blogs(self):
       return Blog.find_by_author_id(self._id)

    def new_blog(self,title,description):
        blog=Blog(self.email,title,description,self._id)
    @staticmethod
    def new_post(blog_id,title,content,date=datetime.datetime.utcnow()):
        blog = Blog.get_from_mongo(blog_id)
        blog.new_post(title, content, date)
