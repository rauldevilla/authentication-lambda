import json

from auth.authenticator import Authenticator

def test_authenticate():
    #ARRANGE
    test_cases:list = [
        {
            'credentials': {
                'login': 'raul.devilla',
                'password': 'abc'
            },
            'is_valid': True
        },
        {
            'credentials': {
                'login': 'bad.user',
                'password': 'no_password'
            },
            'is_valid': False
        }
    ]
    
    authenticator:Authenticator = Authenticator()
    for test_case in test_cases:
        #ACT
        token:str = authenticator.authenticate(test_case["credentials"])

        if test_case["is_valid"]:
            #ASSERT
            assert token != None
        else:
            assert token == None


