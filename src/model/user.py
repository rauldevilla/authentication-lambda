
class User:

    login:str
    password:str
    active:bool

    def __init__(self, login:str = None, password:str = None, active = True) -> None:
        self.login = login
        self.password = password
        self.active = active

    def __str__(self) -> str:
        return f"Login: {self.login}, Active: {self.active}"
