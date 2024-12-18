import sys
import pyautogui
import keyboard
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

originalPause = 0.11
pyautogui.PAUSE = originalPause

# 반복 작업을 변수로 정의
def heal():
    pyautogui.press("3")
    pyautogui.press("3")
    pyautogui.press("2")  # "2" 입력

# 매크로 실행 함수
def run_macro():
    print("매크로 실행 중! F12로 종료하세요.")
    try:
        while True:
            # F12를 눌렀는지 확인하여 루프 종료
            if keyboard.is_pressed("F12"):
                print("F12 키 입력 감지, 프로그램 종료 중...")
                break
            
            # 혼마술
            elif keyboard.is_pressed("q"):  
                # pyautogui.press("esc")  # ESC 입력
                pyautogui.PAUSE = 0.017
                pyautogui.press("4")
                pyautogui.press("up")
                pyautogui.press("enter")
                time.sleep(0.05)
                pyautogui.PAUSE = originalPause
            # 공증 마나없을 때 (F1)
            elif keyboard.is_pressed("F1"):
                time.sleep(0.01)
                pyautogui.press("u")
                pyautogui.press("u")
                pyautogui.press("2")
            
            # 격수 회복 시작(F2)
            elif keyboard.is_pressed("F2"):
                pyautogui.press("tab")
                pyautogui.press("tab")
                heal()  # 반복 작업 호출

            # 격수 회복 (F3)
            elif keyboard.is_pressed("F3"):
                heal()  # 반복 작업 호출
            
            # 자신 치료 (F4)
            elif keyboard.is_pressed("F4"):
                pyautogui.press("esc")  # ESC 입력
                pyautogui.press("3")  # "3" 입력
                pyautogui.press("home")  # Home 입력
                pyautogui.press("enter")  # Enter 입력
                pyautogui.press("3")  # "3" 입력
                pyautogui.press("enter")  # Enter 입력
                pyautogui.press("3")  # "3" 입력
                pyautogui.press("enter")  # Enter 입력
            
            # 공통 대기
            time.sleep(0.01)
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
    script_name = os.path.basename(__file__)  # 현재 실행 중인 파일 이름
    print(f"프로그램 시작. Q를 누르고 있는 동안 매크로 실행. ESC로 종료. 파일 감시 중: {script_name}")

    # 파일 변경 감시 시작
    observer = Observer()
    handler = ChangeHandler(script_name)
    observer.schedule(handler, path=os.path.dirname(os.path.abspath(__file__)), recursive=False)
    observer.start()

    try:
        # 매크로 실행
        run_macro()
    except KeyboardInterrupt:
        print("프로그램 종료됨.")
    finally:
        observer.stop()
        observer.join()
