import os
import json  # JSON 파일 읽기/쓰기용
import time
import threading
import keyboard  # 키보드 모듈 사용
import tkinter as tk
from tkinter import messagebox

# 설정 파일 경로
SETTINGS_FILE = "macro_settings.json"

# 기본 설정값 (초기값)
DEFAULT_SETTINGS = {
    "DEFAULT_DELAY": 0.11,
    "LOW_DELAY": 0.017,
    "heal_count": 3,
    "heal_interval_for_2": 3,
}

# 설정 변수 초기화
DEFAULT_DELAY = DEFAULT_SETTINGS["DEFAULT_DELAY"]
LOW_DELAY = DEFAULT_SETTINGS["LOW_DELAY"]
heal_count = DEFAULT_SETTINGS["heal_count"]
heal_interval_for_2 = DEFAULT_SETTINGS["heal_interval_for_2"]

is_running = False  # 매크로 실행 상태
macro_thread = None  # 매크로 실행 스레드


# 설정 저장 함수
def save_settings():
    settings = {
        "DEFAULT_DELAY": DEFAULT_DELAY,
        "LOW_DELAY": LOW_DELAY,
        "heal_count": heal_count,
        "heal_interval_for_2": heal_interval_for_2,
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


# 설정 불러오기 함수
def load_settings():
    global DEFAULT_DELAY, LOW_DELAY, heal_count, heal_interval_for_2
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)
            DEFAULT_DELAY = settings.get("DEFAULT_DELAY", DEFAULT_DELAY)
            LOW_DELAY = settings.get("LOW_DELAY", LOW_DELAY)
            heal_count = settings.get("heal_count", heal_count)
            heal_interval_for_2 = settings.get("heal_interval_for_2", heal_interval_for_2)


# 키 입력 함수
def press_key(key, delay=None):
    """키를 누르고 지정된 딜레이를 적용 (기본값은 DEFAULT_DELAY)"""
    global DEFAULT_DELAY
    if delay is None:  # delay가 명시되지 않으면 DEFAULT_DELAY 사용
        delay = DEFAULT_DELAY
    keyboard.press_and_release(key)
    time.sleep(delay)


# 동작 정의
def perform_hon_magic():
    # press_key('esc', delay=0.18)
    # press_key('4', delay=0.18)
    # press_key('up', delay=0.18)
    # press_key('enter', delay=0.18)
    press_key('esc', delay=LOW_DELAY)
    press_key('4', delay=LOW_DELAY)
    press_key('up', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)

def heal_target_start():
    press_key('esc')
    press_key('tab')
    press_key('tab')

def heal_target():
    global heal_count, heal_interval_for_2
    print(f"힐 {heal_count}번 실행 중...")
    for i in range(heal_count):  # heal_count 횟수만큼 반복
        press_key('3')
        # 힐 횟수가 설정된 간격(heal_interval_for_2)의 배수일 때 '2' 실행
        if (i + 1) % heal_interval_for_2 == 0:
            press_key('2')

def self_heal():
    press_key('esc')
    press_key('3', delay=LOW_DELAY)
    press_key('home', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)
    time.sleep(0.05)
    press_key('3', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)
    time.sleep(0.05)
    press_key('3', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)

def self_revive():
    press_key('esc')
    press_key('1', delay=LOW_DELAY)
    press_key('home', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)

def mana_recharge():
    press_key('u')
    press_key('u')
    press_key('2')
    press_key('2')
    press_key('2')
    press_key('2')
    press_key('2')

# 매크로 실행 루프
def run_macro():
    global is_running
    print("매크로 실행 중...")
    while is_running:
        try:
            # 혼마술
            if keyboard.is_pressed("q"):
                perform_hon_magic()

            # 마나 회복
            elif keyboard.is_pressed("F1"):
                mana_recharge()

            elif keyboard.is_pressed("right ctrl"):
                press_key('tab')

            # 격수 회복 시작
            elif keyboard.is_pressed("F2"):
                heal_target_start()
                heal_target()

            # 격수 회복
            elif keyboard.is_pressed("F3"):
                heal_target()

            # 자신 치료
            elif keyboard.is_pressed("y"):
                self_heal()
            
            # 자신 부활
            elif keyboard.is_pressed("F4"):
                self_revive()

            time.sleep(0.05)  # 입력 간 대기
        except Exception as e:
            print(f"에러 발생: {e}")
            break

    print("매크로 중단.")
    is_running = False
    status_label.config(text="상태: 중단됨", fg="red")


# 매크로 실행/중단
def toggle_macro():
    global is_running, macro_thread
    if is_running:
        is_running = False
        status_label.config(text="상태: 중단됨", fg="red")
        print("매크로 중단 요청됨.")
    else:
        is_running = True
        status_label.config(text="상태: 실행 중", fg="green")
        macro_thread = threading.Thread(target=run_macro, daemon=True)
        macro_thread.start()
        print("매크로 실행 요청됨.")


# UI 업데이트
def update_settings():
    global DEFAULT_DELAY, LOW_DELAY, heal_count, heal_interval_for_2
    try:
        # 딜레이 값 업데이트
        delay = float(delay_input.get())
        low_delay = float(low_delay_input.get())
        DEFAULT_DELAY = delay
        LOW_DELAY = low_delay
        delay_label.config(text=f"현재 딜레이: {DEFAULT_DELAY:.2f}s")
        low_delay_label.config(text=f"혼마/자힐 딜레이: {LOW_DELAY:.3f}s")

        # 힐 횟수 업데이트
        heal_count = int(heal_count_input.get())
        heal_count_label.config(text=f"현재 힐 횟수: {heal_count}")

        # 힐 간격 업데이트
        heal_interval_for_2 = int(heal_interval_input.get())
        heal_interval_label.config(text=f"공력증강 {heal_interval_for_2}회마다 실행")

        save_settings()  # 설정 저장
        messagebox.showinfo("설정", "설정이 성공적으로 업데이트되었습니다.")
    except ValueError:
        messagebox.showerror("오류", "유효한 숫자를 입력해주세요.")


# UI 생성
def create_ui():
    global delay_input, low_delay_input, heal_count_input, heal_interval_input
    global delay_label, low_delay_label, heal_count_label, heal_interval_label, status_label

    root = tk.Tk()
    root.title("바클 도사 손목 보호 매크로")
    root.geometry("350x780")

    tk.Label(root, text="매크로 설정", font=("Arial", 16)).pack(pady=10)

    # 현재 상태 표시
    status_label = tk.Label(root, text="상태: 중단됨", font=("Arial", 12), fg="red")
    status_label.pack()

    # 현재 딜레이 표시
    delay_label = tk.Label(root, text=f"현재 딜레이: {DEFAULT_DELAY:.2f}s", font=("Arial", 12))
    delay_label.pack()

    low_delay_label = tk.Label(root, text=f"혼마/자힐 딜레이: {LOW_DELAY:.3f}s", font=("Arial", 12))
    low_delay_label.pack()

    # 힐 횟수 표시
    heal_count_label = tk.Label(root, text=f"현재 힐 횟수: {heal_count}", font=("Arial", 12))
    heal_count_label.pack()

    # 힐 간격 표시
    heal_interval_label = tk.Label(root, text=f"공력증강 {heal_interval_for_2}회마다 실행", font=("Arial", 12))
    heal_interval_label.pack()

    # 딜레이 입력 필드
    tk.Label(root, text="기본 딜레이 (초) - 기본 0.11").pack(pady=5)
    delay_input = tk.Entry(root)
    delay_input.insert(0, str(DEFAULT_DELAY))
    delay_input.pack()

    tk.Label(root, text="혼마/자힐 딜레이 (초) - 기본 0.017").pack(pady=5)
    low_delay_input = tk.Entry(root)
    low_delay_input.insert(0, str(LOW_DELAY))
    low_delay_input.pack()

    # 힐 횟수 입력 필드
    tk.Label(root, text="힐 횟수 (기본 3)").pack(pady=5)
    heal_count_input = tk.Entry(root)
    heal_count_input.insert(0, str(heal_count))
    heal_count_input.pack()

    # 힐 간격 입력 필드
    tk.Label(root, text="공력증강 간격 (기본 3)").pack(pady=5)
    heal_interval_input = tk.Entry(root)
    heal_interval_input.insert(0, str(heal_interval_for_2))
    heal_interval_input.pack()

    # 버튼
    tk.Button(root, text="설정 업데이트", command=update_settings).pack(pady=10)
    tk.Button(root, text="매크로 실행/중단", command=toggle_macro).pack(pady=10)

    # 추가 안내 라벨
    tk.Label(root, text="F11로 매크로 실행/중단 가능", font=("Arial", 10)).pack(pady=5)

    keyboard.add_hotkey('F11', toggle_macro)
    tk.Label(root, text="<기본 스킬 설정>", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="2: 공력증강, 3: 회복, 4: 혼마술", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="<단축키>", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="F1: 동동주 먹고 공력증강(동동주 u에 둘 것)", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="F2: 탭탭으로 격수 힐(탭으로 격수 잡아놓을 것)", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="F3: 힐 반복 - F2실행 후 실행", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="F4: 본인 회복시키기", font=("Arial", 12), fg="blue").pack(pady=5)
    tk.Label(root, text="Q: 혼마돌리기", font=("Arial", 12), fg="blue").pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    load_settings()  # 설정 불러오기
    create_ui()
