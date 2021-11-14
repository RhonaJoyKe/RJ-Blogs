from flask import render_template,request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import  User,Blogs,Comment
from .. import db, photos
from ..request import get_quote

from .forms import UpdateProfile,CommentForm,FormBlog
@main.route('/')
def index():
    blogs = Blogs.query.order_by(Blogs.date_created).all()
    quote=get_quote()
    
    return render_template('index.html',blogs=blogs, quote=quote)
@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    form = UpdateProfile()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('.profile',uname=user.username))
    return render_template('profile/update.html',form =form)
@main.route('/createblog', methods=['GET', 'POST'])
@login_required
def new_blog():
    form = FormBlog()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_blog= Blogs(title=title, content=content,user_id=current_user.id)
        new_blog.save_blogs()
        
        return redirect(url_for('main.index'))
    return render_template('blog.html', title='New Post',form = form)

@main.route('/blog/<blog_id>', methods=['GET', 'POST'])
def blog(blog_id):
    blog=Blogs.query.filter_by(id=blog_id).first()
    print(blog)
    return render_template('blogt.html',blog=blog)

# updating a blog
@main.route('/blog/<blog_id>/update',methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog=Blogs.query.filter_by(id=blog_id).first()
    if blog.author.id !=current_user.id:
        abort(403)

    form=FormBlog()
    if form.validate_on_submit():
        blog.title=form.title.data
        blog.content=form.content.data
        db.session.commit()
        flash('Your Post has been Updated','Success')
        return redirect(url_for('.blog',blog_id=blog.id) )
    elif request.method=='GET':
        form.title.data=blog.title
        form.content.data=blog.content
    return render_template('blog.html', form = form,title='Update Post')

@main.route('/blog/<blog_id>/delete',methods=['GET', 'POST'])
@login_required
def delete_blog(blog_id):
    blog=Blogs.query.filter_by(id=blog_id).first()
    if blog.author.id !=current_user.id:
        abort(403)
    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/user/<uname>/update/pic',methods= ['POST'])

def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
@main.route('/comments/<blog_id>', methods=['GET', 'POST'])
@login_required
def comments(blog_id):
    comments = Comment.query.filter_by(blog_id=blog_id).all()
    blog = Blogs.query.get(blog_id)
    form = CommentForm()
    if blog is None:
        abort(404)
    if form.validate_on_submit():
            comment = Comment(
            content=form.content.data,
            blog_id=blog_id,
            user_id=current_user.id
        )
            db.session.add(comment)
            db.session.commit()
            form.content.data = ''
            flash('Your comment has been posted successfully!')
    return render_template('comments.html',blogs= blog, comment=comments, form = form)
@main.route('/comment/<comment_id>', methods=['POST','GET'])
def delete_comment(comment_id):
    comment = Comment.query.filter_by(id = comment_id).first()
    blog_id = comment.blog_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.blog',blog_id = blog_id))