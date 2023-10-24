from enum import Enum
import json
import os

from auth.authenticator import Authenticator
from logger.app_logger import AppLogger

class HTTP_METHOD(Enum):
    OPTIONS = "OPTIONS"
    POST = "POST"

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

def __is_valid_http_method__(method:str) -> bool:
    return method in [HTTP_METHOD.OPTIONS.value, HTTP_METHOD.POST.value]

def __build_credentials_from_event__(event:any) -> dict:
    body:any = None

    try:
        body = event['body']
    except Exception as e:
        AppLogger.error(f"Error geting body from event: {e}")
        return None
    
    if not isinstance(body, dict):
        body = json.loads(body)

    credentials:dict = None
    try:
        credentials = {
            'login': body['login'] if 'login' in body else None,
            'password': body['password'] if 'password' in body else None
        }
    except Exception as e:
        AppLogger.error(f"Error extracting credentials from body {body}. {e}")

    return credentials

def __authenticate__(event) -> str:
    try:
        credentials:dict = __build_credentials_from_event__(event)
        authenticator:Authenticator = Authenticator()
        AppLogger.debug(f"Authenticating with credentials {credentials} ...")
        return authenticator.authenticate(credentials)
    except Exception as e:
        AppLogger.error(f"Error authenticating.\nEvent:\n{event}\nError:\n{e}")
        return None

def __get_http_method__(event:any) -> str:
    try:
        return event['requestContext']['http']['method']
    except Exception as e:
        AppLogger.error(f"Error getting HTTP method. {e}")
        return None

def __do_options__():
    return {
        'statusCode': 200,
        'body': "OK"
    }

def __do_post__(event):
    try:
        token:str = __authenticate__(event)
        if token:
            return {
                'statusCode': 200,
                'body': token
            }
        else:
            return {
                'statusCode': 403, 
                'body': 'Unathorized'
            }
        
    except Exception as e:
        AppLogger.error(str(e))
        return {
            'statusCode': 500,
            'body': 'Unknown error'
        }

def lambda_handler(event:any, context:any) -> any:
    
    response = __validate_api_key__(event)
    if response:
        return response
    
    http_method:str = __get_http_method__(event)
    if http_method == HTTP_METHOD.OPTIONS.value:
        options_response = __do_options__()
        AppLogger.debug(f"Returnig OPTIONS {options_response} ...")
        return options_response
    elif http_method == HTTP_METHOD.POST.value:
        return __do_post__(event)
    else:
        return {
            'statusCode': 403, 
            'body': f'Method {http_method} not authorized'
        }
# if __name__ == "__main__":
#     context:any = None
#     event:any = None
#     lambda_handler(event, context)