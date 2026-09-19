import uuid

client_id = str(uuid.uuid4())

game_state = {
    'mode': 'local',
    'current_player': 'X',
    'my_symbol': 'X',
    'is_my_turn': True,
    'room_code': None,
    'board_data': []
}

questions = [
    {'q': 'Which keyword is used to define a function in Python?', 'ans': 'def'},
    {'q': 'Which keyword is used to send a value back from a function?', 'ans': 'return'},
    {'q': 'What keyword is used to create an anonymous (one-line) function?', 'ans': 'lambda'},
    {'q': 'What are the variables listed inside the function definition parentheses called?', 'ans': 'parameters'},
    {'q': 'What are the actual values passed to a function when it is called called?', 'ans': 'arguments'},
    {'q': 'What keyword is used as a placeholder for a function body that will be written later?', 'ans': 'pass'},
    {'q': 'What symbol is used before a parameter name to accept multiple positional arguments?', 'ans': '*args'},
    {'q': 'What symbol is used before a parameter name to accept multiple keyword arguments?', 'ans': '**kwargs'},
    {'q': 'What built-in function is used to view documentation or info about another function?', 'ans': 'help'},
    {'q': 'What keyword is used to delete a function definition?', 'ans': 'del'},
    {'q': 'What built-in data type in Python is commonly used like an array to store items?', 'ans': 'list'}
]