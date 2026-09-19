import random

def check_winner(game_state):
    win_combos = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    board = game_state['board_data']
    for a, b, c in win_combos:
        if board[a]['status'] == board[b]['status'] == board[c]['status'] and board[a]['status'] in ('X', 'O'):
            return True
    return False

def check_draw(game_state):
    return not any((item['status'] in ('available', 'OPEN') for item in game_state['board_data']))

def start_game(mode, game_state, questions):
    game_state['mode'] = mode
    game_state['my_symbol'] = 'X'
    game_state['is_my_turn'] = True
    game_state['current_player'] = 'X'
    sample_count = min(9, len(questions))
    chosen_questions = random.sample(questions, sample_count)
    random.shuffle(chosen_questions)
    board = []
    for item in chosen_questions:
        board.append({'q': item['q'], 'ans': item['ans'], 'status': 'available'})
    game_state['board_data'] = board