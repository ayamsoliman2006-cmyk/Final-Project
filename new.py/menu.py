import flet as ft

def show_alert(page, title_text):
    dlg = ft.AlertDialog(title=ft.Text(title_text, size=16, weight=ft.FontWeight.BOLD), bgcolor='#F4EEFF')
    page.dialog = dlg
    dlg.open = True
    page.update()

def show_welcome(page, on_start):
    page.clean()
    lbl_welcome = ft.Text('✨ Welcome to our game ✨', size=20, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    title = ft.Text('AXOPY 🎮', size=42, weight=ft.FontWeight.BOLD, color='#FF85A1', text_align=ft.TextAlign.CENTER)
    btn_start = ft.Button(content=ft.Text('🚀 START GAME', size=16, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFB5A7', width=280, height=55, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_start)
    footer = ft.Text('Get ready to test your Python knowledge & tactics!', size=11, color='#3498DB', text_align=ft.TextAlign.CENTER)
    content = ft.Column([ft.Container(height=40), lbl_welcome, ft.Container(height=10), title, ft.Container(height=40), btn_start, ft.Container(height=60), footer], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)

def show_main_menu(page, on_local, on_ai, on_online, on_back):
    page.clean()
    title = ft.Text('🎮 Main Menu', size=26, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    btn_local = ft.Button(content=ft.Text('👥 Local Multiplayer (2P)', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFB5A7', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_local)
    btn_ai = ft.Button(content=ft.Text('🤖 Play vs Computer', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#9BF6FF', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_ai)
    btn_online = ft.Button(content=ft.Text('🌐 Online Multiplayer', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FDFFB6', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_online)
    btn_back = ft.Button(content=ft.Text('⬅ Back to Welcome', size=11, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#CAFFBF', width=200, height=40, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_back)
    content = ft.Column([title, ft.Container(height=20), btn_local, ft.Container(height=10), btn_ai, ft.Container(height=10), btn_online, ft.Container(height=25), btn_back], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)

def show_online_menu(page, on_host, on_join, on_back):
    page.clean()
    title = ft.Text('🌐 Online Game Settings', size=24, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    desc = ft.Text('Host a new game room or join an existing room code.', size=11, color='#3498DB', text_align=ft.TextAlign.CENTER)
    btn_host = ft.Button(content=ft.Text('🏠 Host Game', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#9BF6FF', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_host)
    btn_join = ft.Button(content=ft.Text('🔗 Join Game', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFB5A7', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_join)
    btn_back = ft.Button(content=ft.Text('⬅ Back', size=12, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#CAFFBF', width=180, height=40, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_back)
    content = ft.Column([title, ft.Container(height=10), desc, ft.Container(height=25), btn_host, ft.Container(height=15), btn_join, ft.Container(height=25), btn_back], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)

def show_join_screen(page, on_connect_click, on_back):
    page.clean()
    title = ft.Text('🔗 Join Online Game', size=24, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    desc = ft.Text('Enter the 4-digit room code provided by your friend.', size=12, color='#3498DB', text_align=ft.TextAlign.CENTER)
    code_input = ft.TextField(label='Enter Room Code', width=260, height=50, text_align=ft.TextAlign.CENTER, border_radius=8, bgcolor='#FFFFFF')
    
    btn_connect = ft.Button(content=ft.Text('🚀 Connect', size=14, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#9BF6FF', width=260, height=50, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=lambda e: on_connect_click(code_input.value))
    btn_back = ft.Button(content=ft.Text('⬅ Back', size=12, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#CAFFBF', width=180, height=40, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_back)
    content = ft.Column([title, ft.Container(height=10), desc, ft.Container(height=25), code_input, ft.Container(height=20), btn_connect, ft.Container(height=15), btn_back], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)

def show_waiting_screen(page, text, on_cancel):
    page.clean()
    lbl = ft.Text(text, size=16, weight=ft.FontWeight.BOLD, color='#8E44AD', text_align=ft.TextAlign.CENTER)
    btn_back = ft.Button(content=ft.Text('Cancel', size=12, weight=ft.FontWeight.BOLD, color='#2C2C54'), bgcolor='#FFB5A7', width=150, height=40, style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)), on_click=on_cancel)
    content = ft.Column([lbl, ft.Container(height=30), btn_back], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    page.add(content)