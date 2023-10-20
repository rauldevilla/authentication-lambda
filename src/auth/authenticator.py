
class Authenticator:

    def __valid_credentials__(self, credentials:dict) -> bool:
        if not credentials:
            return False
        
        if not "login" in credentials:
            return False
        
        if not "password" in credentials:
            return False
        
        return True

    def authenticate(self, credentials:dict) -> str:

        if not self.__valid_credentials__(credentials):
            return None

        if credentials["login"] == "raul.devilla" and credentials["password"] == "abc":
            return "123abc456"
        
        return None