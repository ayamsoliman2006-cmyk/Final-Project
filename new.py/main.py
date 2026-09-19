import os
import flet as ft
import asyncio
import random

from mod import game_state, questions, client_id
from menu import show_welcome, show_main_menu, show_online_menu, show_join_screen, show_waiting_screen, show_alert
from board import init_board_ui, show_question_screen, show_game_over_screen
from ctrl import start_game, check_winner, check_draw
from net import host_game, global_pubsub_listener

def main(page: ft.Page):
    page.title = 'AXOPY - Game to learn'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = '#F4EEFF'

    page.on_menu_click_callback = lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_))
    page.on_cancel_to_menu = lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_))
    
    def back_to_welcome(e):
        show_welcome(page, lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_)))

    def show_online_menu_ui(e):
        show_online_menu(
            page, 
            on_host=lambda _: (host_game(page)), 
            on_join=lambda _: show_join_screen(page, on_connect_click=join_action, on_back=lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_))),
            on_back=lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_))
        )

    def join_action(code):
        if code and code.strip() != '':
            game_state['mode'] = 'online'
            game_state['my_symbol'] = 'O'
            game_state['is_my_turn'] = False
            game_state['room_code'] = code.strip()
            page.pubsub.send_all({'sender': client_id, 'type': 'join_room', 'room': code.strip()})
            show_waiting_screen(page, 'Connected to room!\nWaiting for host to start...', lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_)))
        else:
            show_alert(page, 'Please enter a valid room code!')

    def start_local(e):
        start_game('local', game_state, questions)
        init_board_ui(page, 'local', game_state, on_cell_click, page.on_menu_click_callback)

    def start_ai(e):
        start_game('ai', game_state, questions)
        init_board_ui(page, 'ai', game_state, on_cell_click, page.on_menu_click_callback)

    page.on_cell_click_callback = lambda idx: make_move(idx)

    def make_move(idx):
        if game_state['mode'] == 'online' and not game_state['is_my_turn']:
            show_alert(page, "It's not your turn! Wait for your opponent.")
            return
        item = game_state['board_data'][idx]
        if item['status'] in ('X', 'O'):
            show_alert(page, 'This cell is already occupied!')
            return
        show_question_screen(page, idx, game_state, submit_answer, skip_answer)

    def submit_answer(idx, user_ans):
        item = game_state['board_data'][idx]
        if user_ans is None or user_ans.strip() == '':
            item['status'] = 'OPEN'
            handle_turn_end(idx, 'OPEN')
            return
        if user_ans.strip().lower() == item['ans'].lower():
            winner_symbol = game_state['current_player'] if game_state['mode'] != 'online' else game_state['my_symbol']
            item['status'] = winner_symbol
            if check_winner(game_state):
                if game_state['mode'] == 'online':
                    page.pubsub.send_all({'sender': client_id, 'type': 'move', 'room': game_state['room_code'], 'idx': idx, 'status': winner_symbol})
                show_game_over_screen(page, f'Congratulations Player {winner_symbol}!', page.on_menu_click_callback)
                return
            if check_draw(game_state):
                if game_state['mode'] == 'online':
                    page.pubsub.send_all({'sender': client_id, 'type': 'move', 'room': game_state['room_code'], 'idx': idx, 'status': winner_symbol})
                show_game_over_screen(page, "It's a Draw!", page.on_menu_click_callback)
                return
            handle_turn_end(idx, winner_symbol)
        else:
            item['status'] = 'OPEN'
            if check_draw(game_state):
                if game_state['mode'] == 'online':
                    page.pubsub.send_all({'sender': client_id, 'type': 'move', 'room': game_state['room_code'], 'idx': idx, 'status': 'OPEN'})
                show_game_over_screen(page, "It's a Draw!", page.on_menu_click_callback)
                return
            handle_turn_end(idx, 'OPEN')

    def skip_answer(idx):
        game_state['board_data'][idx]['status'] = 'OPEN'
        handle_turn_end(idx, 'OPEN')

    def on_cell_click(idx):
        make_move(idx)

    def handle_turn_end(idx, status):
        if game_state['mode'] == 'online':
            page.pubsub.send_all({'sender': client_id, 'type': 'move', 'room': game_state['room_code'], 'idx': idx, 'status': status})
            game_state['is_my_turn'] = False
            init_board_ui(page, 'online', game_state, page.on_cell_click_callback, page.on_menu_click_callback)
        elif game_state['mode'] == 'ai':
            game_state['current_player'] = 'O'
            init_board_ui(page, 'ai', game_state, on_cell_click, page.on_menu_click_callback)
            page.run_task(ai_turn_delay)
        else:
            game_state['current_player'] = 'O' if game_state['current_player'] == 'X' else 'X'
            init_board_ui(page, 'local', game_state, on_cell_click, page.on_menu_click_callback)

    async def ai_turn_delay():
        await asyncio.sleep(0.8)
        available = [i for i, item in enumerate(game_state['board_data']) if item['status'] not in ('X', 'O')]
        if not available:
            return
        ai_choice = random.choice(available)
        item = game_state['board_data'][ai_choice]
        correct = random.choice([True, False])
        if correct:
            item['status'] = 'O'
            if check_winner(game_state):
                show_game_over_screen(page, 'Congratulations Player O!', page.on_menu_click_callback)
                return
        else:
            item['status'] = 'OPEN'
            show_alert(page, 'Computer made a mistake and the cell text is now visible!')
        if check_draw(game_state):
            show_game_over_screen(page, "It's a Draw!", page.on_menu_click_callback)
            return
        game_state['current_player'] = 'X'
        init_board_ui(page, 'ai', game_state, on_cell_click, page.on_menu_click_callback)

    page.pubsub.subscribe(lambda msg: global_pubsub_listener(msg, page, check_winner, check_draw))
    show_welcome(page, lambda _: show_main_menu(page, lambda _: start_local(_), lambda _: start_ai(_), lambda _: show_online_menu_ui(_), lambda _: back_to_welcome(_)))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    if 'PORT' in os.environ:
        ft.run(main, port=port, host='0.0.0.0')
    else:
        ft.run(main, port=port, host='127.0.0.1', view=ft.AppView.WEB_BROWSER)
        """
AXOPY/
│
├── main.py                  # Entry Point & Application Runner
├── models/
│   └── game_model.py        # Game data, questions, and board state
├── views/
│   ├── menu_views.py        # Welcome screens, main menu, and online menus
│   └── board_views.py       # Game board, question dialogs, and game-over screens
└── controllers/
    ├── game_controller.py   # Game logic (local, vs AI, win/draw conditions)
    └── online_controller.py # Networking and PubSub logic for online mode
"""

import os
import flet as ft
import asyncio
import random

# ... The rest of your code continues from here