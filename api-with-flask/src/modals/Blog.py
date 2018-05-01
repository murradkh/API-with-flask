import uuid
from src.modals.post import Post
from src.modals.database import Database
class Blog(object):
    def __init__(self,author,title,description,author_id,_id=None):
        self.author=author
        self.title=title
        self.description=description
        self.author_id=author_id
        if _id is None:
            self._id=uuid.uuid4().hex
        else:
            self._id=_id

    def new_post(self,title,content,date):
        # title=input("Enter post title: ")
        # content=input("Enter Post content: ")
        # date=input("Enter post date, or leave it blank for today")
        if date is "":
           post=Post(title,content,self.author,self._id)
        else:
           post=Post(title,content,self.author,self._id,date)

        post.save_to_mong()

    def get_posts(self):
        posts=[]
        Posts=Database.find("posts",{"blog_id":self.author_id})
        for y in Posts:
            posts.append(y)
        return posts

    def save_to_mongo(self):
        Database.insert("Blogs",self.json())

    def json(self):
        return {"author":self.author,
                "title":self.title,
                "description":self.description,
                "_id":self._id,
                "author_id":self.author_id
        }
    @staticmethod
    def get_from_mongo(_id):
        blog_data=  Database.find_one("Blogs",{"_id":_id})
        if blog_data is not None:
            return Blog(blog_data['author'],blog_data['title'],blog_data['description'],blog_data['_id'])


    @staticmethod
    def find_by_author_id(author_id):

         return Database.find("Blogs",{"author_id":author_id})
