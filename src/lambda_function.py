import json
import logging
import boto3

from auth.authenticator import Authenticator

KEYS = ['7qo2u4fbasd98ahusdivasdu8']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def __validate_api_key__(event):
    key = None

    try:
        key = event['headers']['api-key']
    except:
        key = None

    if not key or not key in KEYS:
        return {'statusCode': 403, 'body': 'Unauthorized'}
            
    return None

def __is_valid_http_method__(event) -> bool:
    try:
        return event['requestContext']['http']['method'] == 'POST'
    except:
        logger.error(f'Event format is invalid {event}')
        return False

def __build_credentials_from_event__(event:any) -> dict:
    body:any = None

    try:
        body = event['body']
    except:
        return None
    
    if not isinstance(body, dict):
        body = json.loads(body)

    return {
        'login': body['login'] if 'login' in body else None,
        'password': body['password'] if 'password' in body else None
    }

def __authenticate__(event) -> str:
    credentials:dict = __build_credentials_from_event__(event)
    authenticator:Authenticator = Authenticator()
    return authenticator.authenticate(credentials)

def lambda_handler(event:any, context:any) -> any:
    
    logger.debug(str(event))
    
    if not __is_valid_http_method__(event):
        return {'statusCode': 403, 'body': 'Method not authorized'}
    
    try:
        response = __validate_api_key__(event)
        if response:
            return response
        
        token:str = __authenticate__(event['body'])
        if token:
            return {
                'statusCode': 200,
                #'body': json.dumps('Hello from Lambda!')
                'body': token
            }
        else:
            return {'statusCode': 403, 'body': 'Unathorized'}
        
    except Exception as e:
        logger.error(str(e))
        return {
            'statusCode': 500,
            'body': 'Unknown error'
        }

# if __name__ == "__main__":
#     context:any = None
#     event:any = None
#     lambda_handler(event, context)