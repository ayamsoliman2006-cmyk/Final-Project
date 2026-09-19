import random
from mod import client_id, game_state, questions
from board import show_game_over_screen, init_board_ui
from menu import show_waiting_screen

def host_game(page):
    game_state['mode'] = 'online'
    game_state['my_symbol'] = 'X'
    game_state['is_my_turn'] = True
    room_code = str(random.randint(1000, 9999))
    game_state['room_code'] = room_code
    sample_count = min(9, len(questions))
    chosen_questions = random.sample(questions, sample_count)
    random.shuffle(chosen_questions)
    board = []
    for item in chosen_questions:
        board.append({'q': item['q'], 'ans': item['ans'], 'status': 'available'})
    game_state['board_data'] = board
    show_waiting_screen(page, f'Room created! Code: {room_code}\nWaiting for opponent to join...', lambda _: page.on_cancel_to_menu())

def global_pubsub_listener(message, page, check_winner_func, check_draw_func):
    if isinstance(message, dict):
        if message.get('sender') == client_id:
            return
        if game_state['mode'] == 'online' and message.get('room') == game_state['room_code']:
            msg_type = message.get('type')
            if msg_type == 'join_room' and game_state['my_symbol'] == 'X':
                page.pubsub.send_all({'sender': client_id, 'type': 'start_game', 'room': game_state['room_code'], 'board': game_state['board_data']})
                init_board_ui(page, 'online', game_state, page.on_cell_click_callback, page.on_menu_click_callback)
            elif msg_type == 'start_game' and game_state['my_symbol'] == 'O':
                game_state['board_data'] = message['board']
                init_board_ui(page, 'online', game_state, page.on_cell_click_callback, page.on_menu_click_callback)
            elif msg_type == 'move':
                idx = message['idx']
                status = message['status']
                game_state['board_data'][idx]['status'] = status
                if check_winner_func(game_state):
                    show_game_over_screen(page, f'Congratulations Player {status}!', page.on_menu_click_callback)
                    return
                if check_draw_func(game_state):
                    show_game_over_screen(page, "It's a Draw!", page.on_menu_click_callback)
                    return
                game_state['is_my_turn'] = True
                init_board_ui(page, 'online', game_state, page.on_cell_click_callback, page.on_menu_click_callback)