
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.form import PostForm

posts = Blueprint('posts', __name__)


@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def newPost():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # type:ignore
        flash("Your post has been created!", 'success')
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.home'))
    return render_template('createPost.html', title="New Post", form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
def UpdatePost(post_id):
    post = Post.query.get_or_404(post_id)
    # return render_template("post.html", title=post.title, post=post)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has Been Update!", "success")
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET": 
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('createPost.html', title="Update Post", form=form, legend='Update Post')
    
@posts.route('/DeletePost/<int:post_id>', methods = ['POST'])
def DeletePost(post_id):
    post = Post.query.get_or_404(post_id) 
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "danger")
    return redirect(url_for('main.home'))

@posts.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title='404'), 404
