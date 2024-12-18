import keyboard
import threading
import time
import tkinter as tk
from tkinter import messagebox

# 딜레이 기본값
DEFAULT_DELAY = 0.1
is_running = False

# 매크로 실행 루프
def run_macro():
    global is_running
    while is_running:
        if keyboard.is_pressed("q"):
            print("혼마술 실행 중...")
            time.sleep(DEFAULT_DELAY)
        elif keyboard.is_pressed("F1"):
            print("마나 회복 실행 중...")
            time.sleep(DEFAULT_DELAY)
        time.sleep(0.1)

def toggle_macro():
    global is_running
    if is_running:
        is_running = False
        print("매크로 중단됨.")
    else:
        is_running = True
        threading.Thread(target=run_macro, daemon=True).start()
        print("매크로 실행됨.")

# UI 업데이트
def update_delay():
    global DEFAULT_DELAY
    try:
        new_delay = float(delay_input.get())
        DEFAULT_DELAY = new_delay
        delay_label.config(text=f"현재 딜레이: {DEFAULT_DELAY:.2f}초")
        messagebox.showinfo("딜레이 업데이트", "딜레이 설정이 변경되었습니다.")
    except ValueError:
        messagebox.showerror("오류", "유효한 숫자를 입력해주세요.")

# UI 생성
def create_ui():
    global delay_input, delay_label

    root = tk.Tk()
    root.title("매크로 프로그램")
    root.geometry("300x200")

    tk.Label(root, text="매크로 설정", font=("Arial", 16)).pack(pady=10)

    delay_label = tk.Label(root, text=f"현재 딜레이: {DEFAULT_DELAY:.2f}초", font=("Arial", 12))
    delay_label.pack(pady=5)

    tk.Label(root, text="새 딜레이 (초):").pack(pady=5)
    delay_input = tk.Entry(root)
    delay_input.insert(0, str(DEFAULT_DELAY))
    delay_input.pack(pady=5)

    tk.Button(root, text="딜레이 업데이트", command=update_delay).pack(pady=5)
    tk.Button(root, text="매크로 실행/중단", command=toggle_macro).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_ui()
