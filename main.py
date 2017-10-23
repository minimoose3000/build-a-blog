from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:meow@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body = db.Column(db.String(256))
    

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/', methods=['GET'])
def index():
    return redirect('/blog')

@app.route('/blog', methods=['GET'])
def blog():
    view = 'default'
    blogs = []
    blog_id = request.args.get('id')
    if blog_id:
        blogs = Blog.query.filter_by(id=blog_id).first()
        return render_template('index.html', page_title='Build-A-Blog', blogs=[blogs])

        
    else:
        blogs = Blog.query.all()
        return render_template('index.html', page_title='Build-A-Blog', blogs=blogs,)




    

    
@app.route('/new-post', methods=['GET','POST'])
def newpost():
    title = ""
    body = ""
    title_error = ""
    body_error = ""

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        

        if not len(title) > 0:
            title_error = "title cannot be blank"

        if not len(body) > 0:
            body_error = "body cannot be empty"
                
        
        
        if not (title_error) and not (body_error): 
            new_post = Blog(title = title, body = body)
            db.session.add(new_post)
            db.session.commit()
            
            return redirect('/blog?id='+ str(new_post.id))      

        
    return render_template('new-post.html', page_title = "Add a Blog Post")
 #title = title,
       # title_error = title_error, body_error=body_error)
    


 

if __name__ == '__main__':
    app.run()