from flask import render_template, request, Blueprint
from flaskblog.models import Post

main = Blueprint('main', __name__)



@main.route("/")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.datePosted.desc()).paginate(per_page=2, page=page)
    for pagen in posts.iter_pages():  
        print(pagen)
    return render_template('index.html', posts=posts, title='Home')

@main.route("/about")
def about():
    return render_template('about.html', title='About')
