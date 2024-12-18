import os
import sys
import time
import keyboard  # keyboard 모듈 사용
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

DEFAULT_DELAY = 0.11  # 기본 딜레이 (80ms)
LOW_DELAY = 0.017

# 상태 변수
is_f3_running = False  # F3 상태를 관리하는 변수
is_running = True  # 프로그램 실행 상태


# 키 입력 함수
def press_key(key, delay=DEFAULT_DELAY):
    """키를 누르고 지정된 딜레이를 적용"""
    global DEFAULT_DELAY
    if delay is None:
        delay = DEFAULT_DELAY
    keyboard.press_and_release(key)
    time.sleep(delay)


# 동작 정의
def perform_hon_magic():
    """혼마술 동작"""
    print("혼마술 실행 중...")
    press_key('esc', delay=LOW_DELAY)
    press_key('4', delay=LOW_DELAY)
    press_key('up', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)

def heal_target_start():
    """힐 대상 선택"""
    press_key('tab')
    press_key('tab')

def heal_target():
    """힐 동작 반복"""
    press_key('3')
    press_key('3')
    press_key('3')
    press_key('3')
    press_key('2')

def self_heal():
    """자기 자신 힐"""
    press_key('esc')
    press_key('3', delay=LOW_DELAY)
    press_key('home', delay=LOW_DELAY)
    press_key('enter', delay=LOW_DELAY)

def mana_recharge():
    """마나 회복"""
    press_key('u')
    press_key('u')
    press_key('2')
    press_key('2')
    press_key('2')
    press_key('2')
    press_key('2')


# F3 실행/중단 토글 함수
def toggle_f3():
    """F3 상태를 토글"""
    global is_f3_running
    is_f3_running = not is_f3_running
    print(f"F3 반복 {'시작' if is_f3_running else '중단'}")


# 종료 함수
def exit_program():
    """프로그램 종료"""
    global is_running
    is_running = False
    print("프로그램 종료 요청됨.")


# 매크로 실행
def run_macro():
    """매크로 실행 루프"""
    global is_running, is_f3_running
    print("매크로 실행 중! F11로 종료하세요.")

    try:
        while is_running:
            # 혼마술
            if keyboard.is_pressed("q"):
                perform_hon_magic()

            # 마나 회복
            elif keyboard.is_pressed("F1"):
                mana_recharge()

            # 격수 회복 시작
            elif keyboard.is_pressed("F2"):
                heal_target_start()
                heal_target()

            # 격수 회복 (F3 반복 실행)
            if is_f3_running:
                heal_target()

            # 자신 치료
            elif keyboard.is_pressed("F4"):
                self_heal()

            # 입력 간 대기
            time.sleep(0.05)
    except Exception as e:
        print(f"에러 발생: {e}")
    finally:
        print("프로그램이 종료되었습니다.")


# 파일 변경 감지 핸들러
class ChangeHandler(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name

    def on_modified(self, event):
        if event.src_path.endswith(self.script_name):
            print(f"파일 변경 감지됨: {event.src_path}")
            print("프로그램을 재시작합니다.")
            os.execv(sys.executable, ['python'] + [self.script_name])


if __name__ == "__main__":
    script_name = os.path.basename(__file__)
    print(f"매크로 프로그램 시작. Q/F1/F2/F3/F4로 동작, F11로 종료. 파일 감시 중: {script_name}")

    # 핫키 등록
    keyboard.add_hotkey("F3", toggle_f3)  # F3 토글
    keyboard.add_hotkey("F11", exit_program)  # F12 종료

    # 파일 변경 감시 시작
    observer = Observer()
    handler = ChangeHandler(script_name)
    observer.schedule(handler, path=os.path.dirname(os.path.abspath(__file__)), recursive=False)
    observer.start()

    try:
        run_macro()
    except KeyboardInterrupt:
        print("프로그램 종료됨.")
    finally:
        observer.stop()
        observer.join()
