import uuid
from dao.users_dao import UsersDAO
from model.user import User

class Authenticator:

    def __valid_credentials__(self, credentials:dict) -> bool:
        if not credentials:
            return False
        
        if not "login" in credentials:
            return False
        
        if not "password" in credentials:
            return False
        
        return True

    def __compare_credentials__(user:User, credentials:dict) -> bool:
        return  user.login == credentials["login"] and \
                user.password == credentials["password"]

    def authenticate(self, credentials:dict) -> str:

        if not self.__valid_credentials__(credentials):
            return None

        dao_users:UsersDAO = UsersDAO()
        user:User = dao_users.get(credentials.login)
        if not user:
            return None
        
        if self.__compare_credentials__(user, credentials):
            return uuid.uuid4()
        
        return None