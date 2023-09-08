from random import randint

async def generator_expression():
    num1 = randint(20, 40)
    num2 = randint(2, 4)
    num3 = randint(50, 75)
    return {'expression' : f'{num1} * {num2} + {num3}', 'result' : str(num1*num2 + num3)}