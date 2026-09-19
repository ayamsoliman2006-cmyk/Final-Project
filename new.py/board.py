import flet as ft

def show_game_over_screen(page, message_text, on_menu_click):
    page.clean()
    title = ft.Text('🏆 GAME OVER 🏆', size=26, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    msg = ft.Text(message_text, size=22, weight=ft.FontWeight.BOLD, color='#FF85A1', text_align=ft.TextAlign.CENTER)
    btn_menu = ft.Button(content=ft.Text('🏠 Return to Main Menu', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFB5A7', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_menu_click)
    content = ft.Column([title, ft.Container(height=20), msg, ft.Container(height=40), btn_menu], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)

def init_board_ui(page, mode, game_state, on_cell_click, on_menu_click):
    page.clean()
    if mode != 'online':
        status_text = f"Player Turn: {game_state['current_player']}"
    else:
        turn_str = 'Your Turn' if game_state['is_my_turn'] else 'Opponent Turn'
        status_text = f"Your Symbol: {game_state['my_symbol']} ({turn_str})"
        
    info_label = ft.Text(status_text, size=16, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    grid_rows = []
    for r in range(3):
        row_btns = []
        for c in range(3):
            idx = r * 3 + c
            item = game_state['board_data'][idx]
            btn_text = 'Q'
            btn_bg = '#BDB2FF'
            btn_fg = '#2C2C54'
            font_size = 18
            weight = ft.FontWeight.BOLD
            if item['status'] in ('X', 'O'):
                btn_text = item['status']
                btn_bg = '#FFB5A7' if item['status'] == 'X' else '#9BF6FF'
                font_size = 22
            elif item['status'] == 'OPEN':
                btn_text = item['q']
                btn_bg = '#FDFFB6'
                font_size = 9
                weight = ft.FontWeight.W_500
            b = ft.Button(content=ft.Text(btn_text, size=font_size, weight=weight, color=btn_fg, text_align=ft.TextAlign.CENTER), bgcolor=btn_bg, width=110, height=100, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e, i=idx: on_cell_click(i))
            row_btns.append(b)
        grid_rows.append(ft.Row(row_btns, alignment=ft.MainAxisAlignment.CENTER, spacing=6))
    back_btn = ft.Button(content=ft.Text('🏠 Main Menu', size=12, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFC6FF', width=160, height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_menu_click)
    content = ft.Column([info_label, ft.Container(height=10), *grid_rows, ft.Container(height=15), back_btn], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)

def show_question_screen(page, idx, game_state, on_submit, on_skip):
    page.clean()
    item = game_state['board_data'][idx]
    is_open = item['status'] == 'OPEN'
    title_text = f'Cell {idx + 1} Question (Open)' if is_open else 'Python Question 💡'
    title = ft.Text(title_text, size=22, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    q_label = ft.Text(item['q'], size=16, weight=ft.FontWeight.W_500, color='#2C2C54', text_align=ft.TextAlign.CENTER)
    ans_input = ft.TextField(label='Type your answer here...', width=320, text_align=ft.TextAlign.CENTER, border_radius=8)

    btn_submit = ft.Button(content=ft.Text('✅ Submit Answer', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#9BF6FF', width=240, height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: on_submit(idx, ans_input.value))
    btn_skip = ft.Button(content=ft.Text('⏭ Pass / Skip Question', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFB5A7', width=240, height=45, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: on_skip(idx))
    
    content = ft.Column([ft.Container(height=30), title, ft.Container(height=20), q_label, ft.Container(height=25), ans_input, ft.Container(height=20), btn_submit, ft.Container(height=10), btn_skip], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)