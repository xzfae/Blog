from flask import Flask, render_template, request, session, redirect, url_for, json
from werkzeug.security import check_password_hash, generate_password_hash
from data import db_session
from data.posts import Post
from data.users import User
from data.comments import Comment
import datetime as dt

app = Flask(__name__)
app.secret_key = ('secret_key')


@app.route('/')
def index():
    con = db_session.create_session()
    return render_template('index.html',
                           title='Web-блог',
                           posts=con.query(Post).order_by(Post.id.desc()).all()
                           )


@app.route('/post/<id>', methods=['GET', 'POST'])
def post(id):
    con = db_session.create_session()
    if request.method == 'POST':
        text = request.form['comment']
        user_id = session['login']
        post_id = id
        date = dt.date.today().strftime("%d.%m.%Y")
        comment = Comment(post_id=post_id, user_id=user_id, text=text, date=date)
        con.add(comment)
        con.commit()
    return render_template('post.html',
                           title='Пост',
                           post=con.query(Post).filter(Post.id == id).first(),
                           comments=con.query(Comment).filter(Comment.post_id == id).order_by(Comment.id.desc()).all()
                           )


@app.route('/about')
def about():
    return render_template('about.html', title='Об авторе')


@app.route('/maps')
def maps():
    return render_template('maps.html', title='Просто страничка')


@app.route('/login', methods=['GET', 'POST'])
def login():
    con = db_session.create_session()
    if request.method == 'POST':
        user = None
        log = request.form['login']
        pas = request.form['password']
        user = con.query(User).filter(User.login == log).first()
        if user and check_password_hash(user.password, pas):
            session['login'] = user.login
            session['role'] = user.role
            if session['role'] == 'admin':
                return redirect(url_for('admin'))
            elif session['role'] == 'user':
                return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Не верный логин или пароль')
    else:
        return render_template('login.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        if request.method == 'POST':
            post_title = request.form['post_title']
            post_date = dt.date.today().strftime("%d.%m.%Y")
            post_text = request.form['post_text']
            if post_title and post_text:
                post = Post(title=post_title, date=post_date, text=post_text)
                con.add(post)
                con.commit()
                return render_template('admin.html', message='Пост добавлен')
            else:
                return render_template('admin.html', message='Нужно правильно заполнить заголовок и текст для поста')
        else:
            return render_template('admin.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        con = db_session.create_session()
        login = request.form['login']
        password = request.form['password']
        user = con.query(User).filter(User.login == login).first()
        if user:
            return render_template('registration.html', message='Данное имя уже занято! Выберите другое')
        if login and password:
            user = User(login=login, password=generate_password_hash(password), role='user')
            con.add(user)
            con.commit()
            return redirect(url_for('login', message='Вы успешно зарегистрированны! Произведите вход'))
        else:
            return render_template('registration.html', message='Заполните поля логин и пароль!')
    else:
        return render_template('registration.html')


@app.route('/admin/posts')
def admin_posts():
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        return render_template('admin_posts.html',
                               posts=con.query(Post).order_by(Post.date.desc()).all()
                               )
    else:
        return redirect(url_for('login'))


@app.route('/admin/del_post/<id>')
def delete_post(id):
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        post = con.query(Post).filter_by(id=id).one()
        con.delete(post)
        con.commit()
        return redirect(url_for('admin_posts'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/users')
def admin_users():
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        return render_template('admin_users.html',
                               users=con.query(User).filter(User.role == 'user').all()
                               )
    else:
        return redirect(url_for('login'))


@app.route('/admin/del_user/<id>')
def delete_user(id):
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        user = con.query(User).filter_by(id=id).one()
        con.delete(user)
        con.commit()
        return redirect(url_for('admin_users'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/comments')
def admin_comments():
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        return render_template('admin_comments.html',
                               comments=con.query(Comment).all()
                               )
    else:
        return redirect(url_for('login'))


@app.route('/admin/del_comment/<id>')
def delete_comment(id):
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        comment = con.query(Comment).filter_by(id=id).one()
        con.delete(comment)
        con.commit()
        return redirect(url_for('admin_comments'))
    else:
        return redirect(url_for('login'))


@app.route('/admin/edit_post/<id>', methods=['GET', 'POST'])
def edit_post(id):
    if session and session['role'] == 'admin':
        con = db_session.create_session()
        if request.method == 'POST':
            post_title = request.form['post_title']
            post_date = dt.date.today().strftime("%d.%m.%Y")
            post_text = request.form['post_text']
            if post_title and post_text:
                con.query(Post).filter_by(id=id).update({'text': post_text,
                                                         'title': post_title})
                con.commit()
        return render_template('edit_post.html',
                               post=con.query(Post).filter_by(id=id).one()
                               )
    else:
        return redirect(url_for('login'))


db_session.global_init('db/database.db')
app.run('127.0.0.1', 8080, debug=True)
