from os import environ
from time import sleep

import sqlalchemy
from flask import Flask, redirect, request
from flask import render_template
from flask import session
from flask_sock import Sock
from dotenv import load_dotenv

import database.database as database
import models.user.user as user
import models.user.repository as user_repo
import models.chat.chat as chat
import models.chat.repository as chat_repo
from form.signup import SignupForm
from form.login import LoginForm
from websocket.chat import handle_connection

load_dotenv()

app = Flask(__name__)

app.secret_key = environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DATABASE_URL")
database.init_app(app)
database.create_all(app)

@app.get('/')
def index():
    return redirect('/home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request)

    if request.method == 'POST':
        repo = user_repo.Repository(database.db.session)

        u = repo.get_by_name(form.username)
        if u is None:
            form.error = "user not found or invalid credentials"
            return render_template('login/login.html', form=form)

        if u.password == form.password:
            session['username'] = u.username
            return redirect('/home')
        else:
            form.error = "user not found or invalid credentials"
            return render_template('login/login.html', form=form)
    else:
        return render_template('login/login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(
        request.form.get("username"),
        request.form.get("email"),
        request.form.get("password")
    )

    if request.method == 'POST':
        u = user.User(
            username=form.username,
            email=form.email,
            password=form.password,
        )

        repo = user_repo.Repository(database.db.session)

        try:
            repo.create(u)
        except sqlalchemy.exc.IntegrityError:
            form.username_error = "username already taken"
            return render_template('signup/signup.html', form=form)

        session['username'] = u.username

        return redirect('/home')
    else:
        return render_template('signup/signup.html', form=form)

@app.get('/home')
def home():
    if 'username' in session:
        repo = chat_repo.Repository(database.db.session)
        chats = repo.select_user_chats(session.get("username"))

        data = {}
        data['chats'] = chats
        data['user'] = session['username']

        return render_template('home/home.html', data=data)
    else:
        return redirect('/login')

@app.post('/chat/create/<userone>/<usertwo>')
def chat_create(userone, usertwo):
    repo = chat_repo.Repository(database.db.session)
    try:
        repo.create_chat(userone, usertwo)
    except sqlalchemy.exc.IntegrityError:
        return "chat already exists or user does not exist", 400

    return "ok"

sock = Sock(app)

@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)

@sock.route('/websocket/create')
def chat(ws):
    if 'username' not in session:
        return "Unauthorized", 401

    target = request.args.get("target")
    if target is None:
        return "No target provided", 400

    repo = chat_repo.Repository(database.db.session)
    sender = session.get('username')
    handle_connection(ws, sender, target, repo)
    return "ok", 1000
