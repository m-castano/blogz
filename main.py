from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:pass@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_text = db.Column(db.String(120))

    def __init__(self, blog_title, blog_text):
        self.blog_title = blog_title
        self.blog_text = blog_text

@app.route('/blog')
def blog():

    post_id = request.args.get('id')
    if post_id == None:
        posts = Blog.query.all()
        return render_template('blog_home.html', title="Build a Blog", posts=posts) 
    else:
        posts = Blog.query.get(post_id)
        return render_template('individual_blog.html', posts=posts)
    
@app.route('/newpost')
def blog_form():
    
    return render_template('add_a_post.html', title='Add a New Blog Post')

@app.route('/newpost', methods=['POST'])
def add_a_post():

    blog_title_error=''
    blog_text_error=''
    
    blog_title = request.form['blog_title']
    blog_text = request.form['blog_text']
    if blog_title=="" and blog_text=="":
        blog_title_error='Please, fill in the title.'
        blog_text_error='Please, write your blog.'
        return render_template('add_a_post.html', title='Add a New Blog Post',
        blog_title_error=blog_title_error, blog_text_error=blog_text_error)
    if blog_title=="" and len(blog_text)!=0:
        blog_title_error='Please, fill in the title.'
        return render_template('add_a_post.html', title='Add a New Blog Post',
        blog_text=blog_text, blog_title_error=blog_title_error)
    else:
        if len(blog_title)!=0 and blog_text=="":
            blog_text_error='Please, write your blog.'
            return render_template('add_a_post.html', title='Add a New Blog Post',
            blog_title=blog_title, blog_text_error=blog_text_error)
        else:
            if not blog_title_error and not blog_text_error:
                new_blog_post= Blog(blog_title, blog_text)
                db.session.add(new_blog_post)
                db.session.commit()
                new_blog_post_id=new_blog_post.id
                # return render_template('individual_blog.html', blog_title=blog_title, blog_text=blog_text)
                return redirect('/blog?id={}'.format(new_blog_post_id))
if __name__ == '__main__':
    app.run()

