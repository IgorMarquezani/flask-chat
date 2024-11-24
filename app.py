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

import models.session.session as user_session
import models.session.repository as session_repo

from form.signup import SignupForm
from form.login import LoginForm

from websocket.chat import private_chat

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
            form.error = "invalid credentials"
            return render_template('login/login.html', form=form)

        if u.password != form.password:
            form.error = "invalid credentials"
            return render_template('login/login.html', form=form)

        session['username'] = u.username

        client_ip = request.remote_addr
        if request.headers.get("X-Forwarded-For"):
            client_ip = request.headers.get("X-Forwarded-For").split(",")[0]

        us: user_session.Session = user_session.Session(
            session.get('username'),
            u.username,
            client_ip
        )

        repo = session_repo.Repository(database.db.session)

        try:
            repo.create(us)
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            return redirect('/home')

        return redirect('/home')
    else:
        return render_template('login/login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(
        request.form.get("username", ""),
        request.form.get("email", ""),
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

        client_ip = request.remote_addr
        if request.headers.get("X-Forwarded-For"):
            client_ip = request.headers.get("X-Forwarded-For").split(",")[0]

        us: user_session.Session = user_session.Session(
            session.get('username'),
            u.username,
            client_ip
        )

        repo = session_repo.Repository(database.db.session)

        try:
            repo.create(us)
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            return redirect("/home")

        return redirect('/home')
    else:
        return render_template('signup/signup.html', form=form)

@app.get('/home')
def home():
    if 'username' in session:
        chat_repository = chat_repo.Repository(database.db.session)

        data = {
            'chats': chat_repository.select_user_chats(session.get("username")),
            'user': session['username'],
        }

        session_repository = session_repo.Repository(database.db.session)

        data['last_chat'] = session_repository.select_last_chat(session.get("username"))

        if data['last_chat']:
            data['last_chat_messages'] = chat_repository.select_chat_messages(session.get("username"), data['last_chat'])

        return render_template('home/home.html', data=data)
    else:
        return redirect('/login')

@app.get('/chat/private/messages/<target>')
def get_private_messages(target):
    if 'username' not in session:
        return 'not logged in', 401

    chat_repository = chat_repo.Repository(database.db.session)

    messages = chat_repository.select_chat_messages(session['username'], target)

    data = {'user': session['username'], 'messages': messages}

    return render_template("home/_messages.html", data=data)


@app.post('/chat/create/<userone>/<usertwo>')
def chat_create(userone, usertwo):
    repo = chat_repo.Repository(database.db.session)
    try:
        repo.create_chat(userone, usertwo)
    except sqlalchemy.exc.IntegrityError:
        return "chat already exists or user does not exist", 400

    return "ok"

sock = Sock(app)

@sock.route('/websocket/create')
def chat(ws):
    if 'username' not in session:
        return "Unauthorized", 401

    target = request.args.get("target")
    if target is None:
        return "No target provided", 400

    private_chat(ws, session.get('username'), target, database.db.session)
    return "ok", 1000
