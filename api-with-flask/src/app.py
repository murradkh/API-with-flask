from flask import Flask, render_template, request, session
from src.modals.post import Post
from src.modals.Blog import Blog
from src.modals.User import User
from src.modals.database import Database

API = Flask(__name__) # '__main__'
API.secret_key = 'murrad'


@API.route('/')
def Hello_method():
    return render_template("home.html")

@API.route('/register')
def register_template():
    return render_template("register.html")

@API.route('/login')
def login_template():
    return render_template("login.html")

@API.route('/auth/login', methods=['POST'])
def login_user():

    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email=email)
        return render_template('profile.html',email=session['email'])
    else:
        User.logout()
        return "Error: wrong email or password."

@API.route('/auth/register',methods=['POST'])
def Register_user():

    email=request.form['email']
    password=request.form['password']
    if email is not '' or password is not '':
     if User.register(email=email,password=password):
       return render_template("profile.html",email=session['email'])
     else:
        return "Error: User exist."
    else:
        return "Error: Username\password fields is empty"

@API.before_first_request
def DBinitilize():
    Database.initilalize()
@API.route('/blogs/<string:user_id>',methods=['GET'])
@API.route('/blogs',methods=['GET','POST'])
def user_blogs(user_id=None):


    if user_id is None:
        user = User.get_by_email(session['email'])
    else:
        user=User.get_by_id(user_id)

    if request.method == 'POST':
        if user_id is None:
          title=request.form['title']
          description=request.form['description']
          user=User.get_by_email(session['email'])
          blog=Blog(session['email'],title,description,user._id)
          blog.save_to_mongo()
        else:
          return "Error: unexpected method POST"

    blogs=user.get_blogs()
    email=user.email
    return  render_template('user_blogs.html',blogs=blogs,email=email)

@API.route('/posts/<string:blog_id>',methods=['GET','POST'])
def blog_posts(blog_id):
    if request.method == 'POST':
        title=request.form['title']
        content=request.form['content']
        new_post=Post(title,content,session['email'],blog_id)
        new_post.save_to_mong()

    blog = Blog.get_from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html',posts=posts,blog_title=blog.title,blog_id=blog_id)


@API.route('/blogs/new',methods=['GET'])
def create_new_blog():
    return render_template("new_blog.html")

@API.route('/posts/new/<string:blog_id>',methods=['GET'])
def create_new_post(blog_id):
    return render_template("new_post.html",blog_id=blog_id)

@API.route('/logout',methods=['GET'])
def logout():
    user=User.get_by_email(session['email'])
    user.logout()
    return "LOGOUT Sucessful"

if __name__=='__main__':
    API.run(port=4990)

