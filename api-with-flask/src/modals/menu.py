from src.modals.database import  Database
from src.modals.Blog import Blog
class Menu(object):
    def __init__(self):

        self.user=input("Enter you author name: ")
        if self._user_has_account():
            print("Welcome back {}".format(self.user))
        else:
            self._prompt_user_for_account()

    def _user_has_account(self):
        blog_data=Database.find_one("Blogs",{'author':self.user})
        if blog_data is None:
            return False
        else:
            self.blog=Blog.get_from_mongo(blog_data['_id'])
            return True

    def _prompt_user_for_account(self):
        title=input("Enter blog title: ")
        description=input("Enter description: ")
        self.blog=Blog(self.user, title, description)
        self.blog.save_to_mongo()

    def run_menu(self):
        read_or_write=input("Do you want to Read (R) or Write (W) blogs?")
        if read_or_write is 'R':
            self._list_blogs()
            self._view_blog()
        elif read_or_write is 'W':
            self.blog.new_post()
        else:
            print("Thank you for blogging!")

    def _list_blogs(self):
        blogs=Database.find("Blogs",{})
        for blog in blogs:
            print("ID: {}, Title:{}, Author:{} ".format(blog['_id'],blog['title'],blog['author']))

    def _view_blog(self):
        blog_to_see=input("Enter the ID of the blog you'd like to read: ")
        blog= Blog.get_from_mongo(blog_to_see)

        if blog is not None:
            posts=blog.get_posts()
            for post in posts:
                print("Date: {}, title: {}\n\n{}".format(post['date'],post['title'],post['content']))
