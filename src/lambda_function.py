import json
import os

from auth.authenticator import Authenticator
from logger.app_logger import AppLogger

def __validate_api_key__(event):
    key = None

    try:
        key = event['headers']['api-key']
    except:
        key = None

    valid_api_key:str = os.environ["API_KEY"]
    if valid_api_key and key != valid_api_key:
        return {'statusCode': 403, 'body': 'Invalid key'}
    
    return None

def __is_valid_http_method__(event) -> bool:
    try:
        return event['requestContext']['http']['method'] == 'POST'
    except:
        AppLogger.error(f'Event format is invalid {event}')
        return False

def __build_credentials_from_event__(event:any) -> dict:
    body:any = None

    try:
        body = event['body']
    except Exception as e:
        AppLogger.error(f"Error geting body from event: {e}")
        return None
    
    if not isinstance(body, dict):
        body = json.loads(body)

    return {
        'login': body['login'] if 'login' in body else None,
        'password': body['password'] if 'password' in body else None
    }

def __authenticate__(event) -> str:
    try:
        credentials:dict = __build_credentials_from_event__(event)
        authenticator:Authenticator = Authenticator()
        AppLogger.debug(f"Authenticating with credentials {credentials} ...")
        return authenticator.authenticate(credentials)
    except Exception as e:
        AppLogger.error(f"Error authenticating.\nEvent:\n{event}\nError:\n{e}")
        return None

def lambda_handler(event:any, context:any) -> any:
    AppLogger.debug(f"Received: {event}")
    if not __is_valid_http_method__(event):
        return {'statusCode': 403, 'body': 'Method not authorized'}
    
    try:
        response = __validate_api_key__(event)
        if response:
            return response
        
        token:str = __authenticate__(event)
        if token:
            return {
                'statusCode': 200,
                'body': token
            }
        else:
            return {'statusCode': 403, 'body': 'Unathorized'}
        
    except Exception as e:
        AppLogger.error(str(e))
        return {
            'statusCode': 500,
            'body': 'Unknown error'
        }

# if __name__ == "__main__":
#     context:any = None
#     event:any = None
#     lambda_handler(event, context)