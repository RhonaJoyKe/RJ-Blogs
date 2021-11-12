from flask import render_template,request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import  User,Blogs,Comment
from .. import db, photos
from .forms import UpdateProfile,CommentForm,FormBlog
@main.route('/')
def index():
    blogs = Blogs.query.order_by(Blogs.date_created).all()
    
    return render_template('index.html',blogs=blogs)
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
# @login_required
def new_blog():
    blog_form = FormBlog()
    if blog_form.validate_on_submit():
        title = blog_form.title.data
        category = blog_form.category.data
        content = blog_form.content.data
        new_blog= Blogs(title=title, category=category, content=content)
        new_blog.save_blogs
        
        return redirect(url_for('main.index'))
    return render_template('blog.html', blog_form = blog_form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
@main.route('/comments/<pitch_id>', methods=['GET', 'POST'])
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
