
from calculator.calculator import Calculator

def test_sum():
    #ARRANGE
    test_cases:list = [
        {
            'op1': 2,
            'op2': 3,
            'exp': 5
        },
        {
            'op1': 2,
            'op2': 1,
            'exp': 3
        }
    ]

    calc:Calculator = Calculator()

    #ACT
    for test_case in test_cases:
        result:int = calc.sum(test_case['op1'], test_case['op2'])

        #ASSERT
        assert result == test_case['exp']