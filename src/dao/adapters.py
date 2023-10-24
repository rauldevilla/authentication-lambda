
from model.user import User

def item_to_user(item:dict) -> User:
    return User(login = item['login'], password = item['password'], active = item['active'])
