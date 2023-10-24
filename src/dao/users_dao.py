import boto3
from dao.adapters import item_to_user
from logger.app_logger import AppLogger
from model.user import User

TABLE_USERS:str = "Users"

class UsersDAO:

    def get(self, login:str) -> User:
        user:User = None

        dynamodb:any = boto3.resource("dynamodb")
        table = dynamodb.Table(TABLE_USERS)

        key:dict = {'login': login}
        AppLogger.debug(f"Getting user {key} ..")
        reponse:any = table.get_item(
            Key = key
        )
        AppLogger.debug(f"Response {reponse} ..")

        item:any = reponse['Item']
        if item:
            user = item_to_user(item)

        return user
