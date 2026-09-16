import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import socket
import threading
import json
from game_logic import QuestionManager

class AXOPYGame:
    def __init__(self, root):
        self.root = root
        self.root.title("AXOPY - Advanced Trivia Tic-Tac-Toe")
        self.root.geometry("680x750")
        self.root.config(bg="#1e1e2f")

        self.qm = QuestionManager("questions.json")
        self.board_data = self.qm.get_random_board_questions()

        self.current_player = "X"
        self.game_mode = "local"
        self.my_symbol = "X"
        self.socket_conn = None
        self.is_my_turn = True
        self.recv_buffer = ""

        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()

        title = tk.Label(self.root, text="⚡ AXOPY ⚡\nAdvanced Python Trivia Challenge", 
                         font=("Arial", 22, "bold"), bg="#1e1e2f", fg="#00ffcc")
        title.pack(pady=30)

        btn_local = tk.Button(self.root, text="👥 Local 2-Player", font=("Arial", 14, "bold"), 
                              bg="#4e54c8", fg="white", width=25, height=2, command=lambda: self.start_game("local"))
        btn_local.pack(pady=10)

        btn_ai = tk.Button(self.root, text="🤖 Vs Computer (AI)", font=("Arial", 14, "bold"), 
                           bg="#00adb5", fg="white", width=25, height=2, command=lambda: self.start_game("ai"))
        btn_ai.pack(pady=10)

        btn_online = tk.Button(self.root, text="🌐 Online Multiplayer", font=("Arial", 14, "bold"), 
                            bg="#ff5722", fg="white", width=25, height=2, command=self.setup_online_menu)
        btn_online.pack(pady=10)

        btn_exit = tk.Button(self.root, text="Exit", font=("Arial", 12), 
                             bg="#d9534f", fg="white", width=15, height=1, command=self.root.quit)
        btn_exit.pack(pady=20)

    def setup_online_menu(self):
        self.clear_window()
        title = tk.Label(self.root, text="🌐 AXOPY Online Setup", font=("Arial", 20, "bold"), bg="#1e1e2f", fg="white")
        title.pack(pady=20)

        desc = tk.Label(self.root, text="Host starts a server or Join via Host IP/Port.\nUse Ngrok for cross-network play.", 
                        font=("Arial", 11), bg="#1e1e2f", fg="#aaa")
        desc.pack(pady=5)

        btn_host = tk.Button(self.root, text="Host Game", font=("Arial", 14, "bold"), bg="#28a745", fg="white", width=24, height=2, command=self.start_host)
        btn_host.pack(pady=15)

        btn_join = tk.Button(self.root, text="Join Game", font=("Arial", 14, "bold"), bg="#17a2b8", fg="white", width=24, height=2, command=self.start_join)
        btn_join.pack(pady=15)

        btn_back = tk.Button(self.root, text="Back", font=("Arial", 12), bg="#555", fg="white", width=15, command=self.create_main_menu)
        btn_back.pack(pady=20)

    def start_host(self):
        self.game_mode = "online"
        self.my_symbol = "X"
        self.is_my_turn = True
        self.recv_buffer = ""

        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', 5555))
            self.server_socket.listen(1)
            messagebox.showinfo("Hosting", "Server running on Port 5555!\nWaiting for opponent...")
            threading.Thread(target=self.accept_connection, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Could not start server: {e}")

    def accept_connection(self):
        try:
            self.server_socket.settimeout(120)
            conn, addr = self.server_socket.accept()
            self.socket_conn = conn
            self.root.after(100, lambda: messagebox.showinfo("Connected", "Opponent joined! Match starting."))
            self.root.after(150, lambda: self.init_board_ui("online"))
            threading.Thread(target=self.receive_data, daemon=True).start()
        except socket.timeout:
            self.root.after(0, lambda: messagebox.showerror("Error", "No connection received within 2 minutes."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Hosting issue: {e}"))

    def start_join(self):
        self.game_mode = "online"
        self.my_symbol = "O"
        self.is_my_turn = False
        self.recv_buffer = ""

        connection_info = simpledialog.askstring("Join Game", "Enter Host IP:Port\n(e.g., 127.0.0.1:5555)", initialvalue="127.0.0.1:5555")
        if not connection_info:
            return

        try:
            parts = connection_info.strip().split(":")
            host = parts[0]
            port = int(parts[1])

            self.socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_conn.settimeout(10)
            self.socket_conn.connect((host, port))
            self.socket_conn.settimeout(None)
            messagebox.showinfo("Success", "Connected to host successfully!")
            self.init_board_ui("online")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Error", f"Connection failed: {e}")

    def start_game(self, mode):
        self.game_mode = mode
        self.my_symbol = "X"
        self.is_my_turn = True
        self.board_data = self.qm.get_random_board_questions()
        self.init_board_ui(mode)

    def init_board_ui(self, mode):
        self.clear_window()
        self.current_player = "X"

        status_text = f"Current Turn: Player {self.current_player}" if mode != "online" else f"You are Playing as: {self.my_symbol}"
        self.info_label = tk.Label(self.root, text=status_text, font=("Arial", 16, "bold"), bg="#1e1e2f", fg="#00ffcc")
        self.info_label.pack(pady=15)

        grid_frame = tk.Frame(self.root, bg="#1e1e2f")
        grid_frame.pack()

        self.buttons = []
        for i in range(9):
            btn = tk.Button(grid_frame, text="Q", font=("Arial", 20, "bold"),
                            width=14, height=4, bg="#2d2d44", fg="white", wraplength=110,
                            command=lambda idx=i: self.make_move(idx))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        back_btn = tk.Button(self.root, text="Return to Main Menu", font=("Arial", 12), bg="#555", fg="white", command=self.close_connection_and_go_home)
        back_btn.pack(pady=20)

    def close_connection_and_go_home(self):
        if self.socket_conn:
            try:
                self.socket_conn.close()
            except Exception:
                pass
            self.socket_conn = None
        self.create_main_menu()

    def make_move(self, idx):
        if self.game_mode == "online" and not self.is_my_turn:
            messagebox.showwarning("Warning", "Not your turn! Wait for opponent.")
            return

        # Disable input during Computer turn
        if self.game_mode == "ai" and self.current_player != "X":
            return

        item = self.board_data[idx]

        if item["status"] in ("X", "O"):
            messagebox.showwarning("Warning", "This tile is already claimed!")
            return

        user_ans = simpledialog.askstring(f"Question {idx+1}", item["q"])

        if user_ans is None:
            item["status"] = "OPEN"
            self.buttons[idx].config(text=item["q"], font=("Arial", 8, "bold"), bg="#ffc107", fg="black")
            messagebox.showinfo("Skipped", "Question skipped! Tile is open for anyone.")

            if self.game_mode == "online":
                self.send_network_data(idx, "OPEN", item["q"])
                self.is_my_turn = False
                self.info_label.config(text="Opponent's Turn...")
            else:
                self.switch_turn()
            return

        if self.qm.validate_answer(user_ans, item["ans"]):
            winner_symbol = self.current_player if self.game_mode != "online" else self.my_symbol
            item["status"] = winner_symbol
            bg_color = "#28a745" if winner_symbol == "X" else "#007bff"
            self.buttons[idx].config(text=winner_symbol, font=("Arial", 24, "bold"), bg=bg_color, fg="white")

            if self.check_winner():
                messagebox.showinfo("Game Over", f"🎉 Winner! Player {winner_symbol} takes the game!")
                if self.game_mode == "online":
                    self.close_connection_and_go_home()
                else:
                    self.start_game(self.game_mode)
                return

            if self.game_mode == "online":
                self.send_network_data(idx, winner_symbol, "")
                self.is_my_turn = False
                self.info_label.config(text="Opponent's Turn...")
            else:
                self.switch_turn()
        else:
            item["status"] = "OPEN"
            self.buttons[idx].config(text=item["q"], font=("Arial", 8, "bold"), bg="#ffc107", fg="black")
            messagebox.showerror("Incorrect", "Incorrect answer! Tile is now open on the board.")

            if self.game_mode == "online":
                self.send_network_data(idx, "OPEN", item["q"])
                self.is_my_turn = False
                self.info_label.config(text="Opponent's Turn...")
            else:
                self.switch_turn()

    def switch_turn(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.info_label.config(text=f"Current Turn: Player {self.current_player}")

        if self.game_mode == "ai" and self.current_player == "O":
            self.root.after(700, self.ai_turn)

    def ai_turn(self):
        available_indices = [i for i, item in enumerate(self.board_data) if item["status"] not in ("X", "O")]
        
        if not available_indices:
            messagebox.showinfo("Game Over", "It's a Draw! No moves left.")
            self.start_game("ai")
            return

        ai_choice = random.choice(available_indices)
        item = self.board_data[ai_choice]

        # 70% chance of correct answer by AI
        correct = random.choices([True, False], weights=[0.7, 0.3])[0]

        if correct:
            item["status"] = "O"
            self.buttons[ai_choice].config(text="O", font=("Arial", 24, "bold"), bg="#007bff", fg="white")
            messagebox.showinfo("AI Move", f"Computer answered correctly on tile {ai_choice+1}!")
            if self.check_winner():
                messagebox.showinfo("Game Over", "🤖 Computer won the match!")
                self.start_game("ai")
                return
        else:
            item["status"] = "OPEN"
            self.buttons[ai_choice].config(text=item["q"], font=("Arial", 8, "bold"), bg="#ffc107", fg="black")
            messagebox.showinfo("AI Move", f"Computer failed to answer tile {ai_choice+1}. Tile is now open!")

        self.switch_turn()

    def send_network_data(self, idx, status, q_text):
        if self.socket_conn:
            try:
                data = json.dumps({"idx": idx, "status": status, "q_text": q_text}) + "\n"
                self.socket_conn.sendall(data.encode('utf-8'))
            except Exception:
                self.root.after(0, lambda: messagebox.showerror("Error", "Connection lost."))

    def receive_data(self):
        while self.socket_conn:
            try:
                chunk = self.socket_conn.recv(4096)
                if not chunk:
                    break
                self.recv_buffer += chunk.decode('utf-8', errors='ignore')

                while "\n" in self.recv_buffer:
                    line, self.recv_buffer = self.recv_buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    packet = json.loads(line)
                    self.root.after(10, lambda p=packet: self.apply_network_move(p))
            except Exception:
                break

        self.socket_conn = None
        self.root.after(0, self.notify_disconnected)

    def notify_disconnected(self):
        messagebox.showwarning("Disconnected", "Opponent disconnected. Returning to main menu.")
        self.create_main_menu()

    def apply_network_move(self, packet):
        idx = packet["idx"]
        status = packet["status"]
        q_text = packet["q_text"]

        item = self.board_data[idx]
        item["status"] = status

        if status in ("X", "O"):
            bg_color = "#28a745" if status == "X" else "#007bff"
            self.buttons[idx].config(text=status, font=("Arial", 24, "bold"), bg=bg_color, fg="white")
        elif status == "OPEN":
            self.buttons[idx].config(text=q_text, font=("Arial", 8, "bold"), bg="#ffc107", fg="black")

        if self.check_winner():
            messagebox.showinfo("Game Over", f"Match finished! Winner: {status}")
            self.close_connection_and_go_home()
            return

        self.is_my_turn = True
        self.info_label.config(text=f"Your Turn! ({self.my_symbol})")

    def check_winner(self):
        win_combos = [
            (0,1,2), (3,4,5), (6,7,8),
            (0,3,6), (1,4,7), (2,5,8),
            (0,4,8), (2,4,6)
        ]
        for a, b, c in win_combos:
            if (self.board_data[a]["status"] == self.board_data[b]["status"] == self.board_data[c]["status"]) and self.board_data[a]["status"] in ("X", "O"):
                return True
        return False

if __name__ == "__main__":
    root = tk.Tk()
    app = AXOPYGame(root)
    root.mainloop()