import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import socket
import threading
import json

class UltimateTriviaTicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("لعبة تيك تاك تو الذكية - المسابقات الكبرى")
        self.root.geometry("650x720")
        self.root.config(bg="#1e1e2f")

        self.current_player = "X"
        self.game_mode = "local"
        self.my_symbol = "X"     
        self.socket_conn = None
        self.is_my_turn = True

        self.board_data = [
            {"q": "ما ناتج 2 ** 3 في بايثون؟", "ans": "8", "status": "available"},
            {"q": "كلمة لإنشاء دالة (Function)؟", "ans": "def", "status": "available"},
            {"q": "نوع بيانات الأعداد الصحيحة؟", "ans": "int", "status": "available"},
            {"q": "حلقة تكرار مشروطة (Loop)؟", "ans": "while", "status": "available"},
            {"q": "ما هي قيمة منطقية صحيحة؟", "ans": "True", "status": "available"},
            {"q": "لإنشاء قائمة نستخدم أقواس؟", "ans": "[]", "status": "available"},
            {"q": "دالة لطباعة نص على الشاشة؟", "ans": "print", "status": "available"},
            {"q": "دالة لقراءة مدخلات المستخدم؟", "ans": "input", "status": "available"},
            {"q": "ما هو امتداد ملفات بايثون؟", "ans": "py", "status": "available"}
        ]

        self.create_main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_main_menu(self):
        self.clear_window()
        
        title = tk.Label(self.root, text="🎮 تحدي تيك تاك تو الذكي", font=("Arial", 22, "bold"), bg="#1e1e2f", fg="white")
        title.pack(pady=30)

        btn_local = tk.Button(self.root, text="👥 لعب محلي (لاعبين)", font=("Arial", 14, "bold"), bg="#4e54c8", fg="white", width=24, height=2, command=lambda: self.start_game("local"))
        btn_local.pack(pady=10)

        btn_ai = tk.Button(self.root, text="🤖 لعب ضد الكمبيوتر", font=("Arial", 14, "bold"), bg="#00adb5", fg="white", width=24, height=2, command=lambda: self.start_game("ai"))
        btn_ai.pack(pady=10)

        btn_online = tk.Button(self.root, text="🌐 لعب أونلاين (شبكات مختلفة)", font=("Arial", 14, "bold"), bg="#ff5722", fg="white", width=24, height=2, command=self.setup_online_menu)
        btn_online.pack(pady=10)

        btn_exit = tk.Button(self.root, text="خروج", font=("Arial", 12), bg="#d9534f", fg="white", width=15, height=1, command=self.root.quit)
        btn_exit.pack(pady=20)

    def setup_online_menu(self):
        self.clear_window()
        title = tk.Label(self.root, text="🌐 إعدادات اللعب أونلاين", font=("Arial", 20, "bold"), bg="#1e1e2f", fg="white")
        title.pack(pady=20)

        desc = tk.Label(self.root, text="للعب على شبكات مختلفة، المضيف يشغل السيرفر\nويستخدم برنامج Ngrok للربط الخارجي.", font=("Arial", 11), bg="#1e1e2f", fg="#aaa")
        desc.pack(pady=5)

        btn_host = tk.Button(self.root, text="استضافة لعبة (Host)", font=("Arial", 14, "bold"), bg="#28a745", fg="white", width=24, height=2, command=self.start_host)
        btn_host.pack(pady=15)

        btn_join = tk.Button(self.root, text="الانضمام لعبة (Join)", font=("Arial", 14, "bold"), bg="#17a2b8", fg="white", width=24, height=2, command=self.start_join)
        btn_join.pack(pady=15)

        btn_back = tk.Button(self.root, text="العودة", font=("Arial", 12), bg="#555", fg="white", width=15, command=self.create_main_menu)
        btn_back.pack(pady=20)

    def start_host(self):
        self.game_mode = "online"
        self.my_symbol = "X"
        self.is_my_turn = True
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', 5555))
            self.server_socket.listen(1)
            messagebox.showinfo("انتظار", "تم فتح السيرفر على البورت 5555!\n\nللعبي على شبكة مختلفة عبر الإنترنت:\nاكتبِ في الـ Terminal عندك:\nngrok tcp 5555\nوابعتي للخصم العنوان اللي هيطلعلك (مثال: 0.tcp.ngrok.io والبورت الخاص به).")
            threading.Thread(target=self.accept_connection, daemon=True).start()
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر فتح السيرفر: {e}")

    def accept_connection(self):
        try:
            conn, addr = self.server_socket.accept()
            self.socket_conn = conn
            self.root.after(100, lambda: messagebox.showinfo("اتصال ناجح", "تم اتصال الخصم بنجاح عبر الإنترنت! تبدأ اللعبة الآن."))
            self.root.after(150, lambda: self.init_board_ui("online"))
            threading.Thread(target=self.receive_data, daemon=True).start()
        except:
            pass

    def start_join(self):
        self.game_mode = "online"
        self.my_symbol = "O"
        self.is_my_turn = False # المضيف يبدأ أولاً
        
        # يتيح إدخال العنوان والبورت المنفصلين ليدعم ngrok أو أي شبكة خارجية
        connection_info = simpledialog.askstring("اتصال", "أدخل عنوان الخصم (Host) ورقم البورت (Port)\nبالشكل التالي (IP:Port أو Host:Port):\nمثال: 0.tcp.ngrok.io:12345", initialvalue="127.0.0.1:5555")
        if not connection_info:
            return

        try:
            parts = connection_info.strip().split(":")
            host = parts[0]
            port = int(parts[1])

            self.socket_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_conn.connect((host, port))
            messagebox.showinfo("اتصال ناجح", "تم الاتصال بالمضيف بنجاح عبر الشبكة الخارجية!")
            self.init_board_ui("online")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل الاتصال: {e}\nتأكد من كتابة العنوان والبورت بشكل صحيح.")

    def start_game(self, mode):
        self.game_mode = mode
        self.my_symbol = "X"
        self.is_my_turn = True
        self.init_board_ui(mode)

    def init_board_ui(self, mode):
        self.clear_window()
        self.current_player = "X"
        
        for item in self.board_data:
            item["status"] = "available"

        status_text = f"دور اللاعب: {self.current_player}" if mode != "online" else f"دورك برمز: {self.my_symbol}"
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

        back_btn = tk.Button(self.root, text="العودة للقائمة الرئيسية", font=("Arial", 12), bg="#555", fg="white", command=self.create_main_menu)
        back_btn.pack(pady=20)

    def make_move(self, idx):
        if self.game_mode == "online" and not self.is_my_turn:
            messagebox.showwarning("تنبيه", "ليس دورك الآن! انتظر دور خصمك.")
            return

        item = self.board_data[idx]
        
        if item["status"] in ("X", "O"):
            messagebox.showwarning("تنبيه", "هذه الخانة محجوزة بالفعل!")
            return

        is_open = (item["status"] == "OPEN")
        prompt_title = f"سؤال الخانة {idx+1} (مفتوح)" if is_open else f"سؤال الخانة {idx+1} (اضغط Cancel للتخطي/باس)"
        
        user_ans = simpledialog.askstring(prompt_title, item["q"])
        
        # لو اللاعب عمل Cancel (تخطي / باس) -> يختفي الـ Q ويظهر السؤال بره
        if user_ans is None:
            item["status"] = "OPEN"
            self.buttons[idx].config(text=item["q"], font=("Arial", 9, "bold"), bg="#ffc107", fg="black")
            messagebox.showinfo("تخطي (Pass)", "تم تخطي السؤال وأصبح مفتوحاً على اللوحة!")
            
            if self.game_mode == "online":
                self.send_network_data(idx, "OPEN", item["q"])
                self.is_my_turn = False
                self.info_label.config(text="دور الخصم...")
            else:
                self.switch_turn()
            return  
        if user_ans.strip() == item["ans"]:
            winner_symbol = self.current_player if self.game_mode != "online" else self.my_symbol
            item["status"] = winner_symbol
            bg_color = "#28a745" if winner_symbol == "X" else "#007bff"
            self.buttons[idx].config(text=winner_symbol, font=("Arial", 24, "bold"), bg=bg_color, fg="white")
            
            if self.check_winner():
                messagebox.showinfo("نهاية اللعبة", f"🎉 الف مبروك! اللاعب {winner_symbol} فاز بالجولة!")
                if self.game_mode == "online":
                    self.create_main_menu()
                else:
                    self.start_game(self.game_mode)
                return

            if self.game_mode == "online":
                self.send_network_data(idx, winner_symbol, "")
                self.is_my_turn = False
                self.info_label.config(text="دور الخصم...")
            else:
                self.switch_turn()
        else:
            item["status"] = "OPEN"
            self.buttons[idx].config(text=item["q"], font=("Arial", 9, "bold"), bg="#ffc107", fg="black")
            messagebox.showerror("خطأ", "إجابة خاطئة! أصبحت الخانة مفتوحة والسؤال ظاهر للجميع.")
            
            if self.game_mode == "online":
                self.send_network_data(idx, "OPEN", item["q"])
                self.is_my_turn = False
                self.info_label.config(text="دور الخصم...")
            else:
                self.switch_turn()

    def switch_turn(self):
        self.current_player = "O" if self.current_player == "X" else "X"
        self.info_label.config(text=f"دور اللاعب: {self.current_player}")

        if self.game_mode == "ai" and self.current_player == "O":
            self.root.after(800, self.ai_turn)

    def ai_turn(self):
        available_indices = [i for i, item in enumerate(self.board_data) if item["status"] not in ("X", "O")]
        if not available_indices:
            return
        
        ai_choice = random.choice(available_indices)
        item = self.board_data[ai_choice]
        
        messagebox.showinfo("دور الكمبيوتر (AI)", f"الكمبيوتر اختار الخانة رقم {ai_choice+1}")
        correct = random.choice([True, False])
        
        if correct:
            item["status"] = "O"
            self.buttons[ai_choice].config(text="O", font=("Arial", 24, "bold"), bg="#007bff", fg="white")
            if self.check_winner():
                messagebox.showinfo("نهاية اللعبة", "🤖 الكمبيوتر فاز بالجولة!")
                self.start_game("ai")
                return
        else:
            item["status"] = "OPEN"
            self.buttons[ai_choice].config(text=item["q"], font=("Arial", 9, "bold"), bg="#ffc107", fg="black")
            messagebox.showinfo("دور الكمبيوتر", "الكمبيوتر أخطأ وأصبحت الخانة مفتوحة بره!")

        self.switch_turn()

    def send_network_data(self, idx, status, q_text):
        if self.socket_conn:
            try:
                data = json.dumps({"idx": idx, "status": status, "q_text": q_text})
                self.socket_conn.sendall(data.encode('utf-8'))
            except Exception as e:
                print(f"Error sending data: {e}")

    def receive_data(self):
        while self.socket_conn:
            try:
                data = self.socket_conn.recv(1024)
                if not data:
                    break
                packet = json.loads(data.decode('utf-8'))
                self.root.after(10, lambda p=packet: self.apply_network_move(p))
            except:
                break

    def apply_network_move(f, packet):
        # correction for self reference in lambda wrapper if needed, handled properly below
        pass

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
            self.buttons[idx].config(text=q_text, font=("Arial", 9, "bold"), bg="#ffc107", fg="black")

        if self.check_winner():
            messagebox.showinfo("نهاية اللعبة", f"انتهت الجولة! الفائز هو {status}")
            self.create_main_menu()
            return

        self.is_my_turn = True
        self.info_label.config(text=f"دورك الآن! ({self.my_symbol})")

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
    app = UltimateTriviaTicTacToe(root)
    root.mainloop()

