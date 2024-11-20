
class SignupForm():
    username: str
    email: str
    password: str
    username_error: str

    def __init__(self, username: None | str, email: None | str, password: None | str):
        self.username = username
        self.email = email
        self.password = password
