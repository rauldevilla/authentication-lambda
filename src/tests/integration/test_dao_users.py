
from dao.users_dao import UsersDAO
from model.user import User

def test_get_user():

    dao_user:UsersDAO = UsersDAO()
    user:User = dao_user.get('raul.devilla@gmail.com')
    print(f"The user is: {user}")
