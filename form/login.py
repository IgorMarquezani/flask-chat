from flask import Request

class LoginForm():
    error: str

    def __init__(self, request: Request):
        self.username = request.form.get('username', "")
        self.password = request.form.get('password')