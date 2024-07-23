from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from functools import wraps
from models import db, User, BlogPost, Comment
from forms import LoginForm, CommentForm, RegistrationForm
from config import Config
import logging
import requests
import threading
#logging.basicConfig()
#logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    posts = BlogPost.query.all()
    print(posts)
    return render_template('index.html', posts=posts)

def visit_admin_site(post_id):
    visit_admin_site = requests.get("http://127.0.0.1:7000/visit_post?query=" + "/post/" + str(post_id))

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
            db.session.add(comment)
            db.session.commit()

            thread = threading.Thread(target=visit_admin_site, args=(post_id,))
            thread.start() 

            flash('Your comment has been added!', 'success')
        else:
            flash('You need to login to comment', 'danger')
    return render_template('post.html', post=post, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/admin')
@login_required
@admin_required
def admin():
    users = User.query.all()
    posts = BlogPost.query.all()
    return render_template('admin.html', users=users, posts=posts)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    comments = Comment.query.filter_by(user_id=user_id).all()
    for comment in comments:
        db.session.delete(comment)

    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted!', 'success')
    return redirect(url_for('admin'))

@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
@admin_required
def delete_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    # Eliminar los comentarios asociados
    Comment.query.filter_by(post_id=post.id).delete()
    # Eliminar el post
    db.session.delete(post)
    db.session.commit()
    flash('Post has been deleted!', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
