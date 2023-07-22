# Quiz) 아래 동작을 자동으로 수행하는 프로그램을 작성하시오

# 1. 그림판 실행 (단축키 : win + r, 입력값 : mspaint) 및 최대화

# 2. 상단의 텍스트 기능을 이용하여 흰 영역 아무 곳에다가 글자 입력
#   - 입력 글자 : "참 잘했어요"
  
# 3. 5초 대기 후 그림판 종료
#   이 때, 저장하지 않음을 자동을 선택하여 프로그램이 완전 종료되도록 함

import pyautogui
import pyperclip
import sys

# 1. 그림판 실행 (단축키 : win + r, 입력값 : mspaint) 및 최대화
pyautogui.hotkey("win", "r")    # 단축키 : win + r 입력
pyautogui.write("mspaint")
pyautogui.press("enter")        # 엔터 키 입력
# pyautogui.hotkey("enter")     # 이렇게 해도 됨

# 그림판 나타날 때까지 2초 대기
pyautogui.sleep(2)

window = pyautogui.getWindowsWithTitle("제목 없음 - 그림판")[0] # 그림판 1개만 띄워져 있다고 가정
if window.isMaximized is False:
    window.maximize()   # 최대화
    
pyautogui.sleep(2)

# 2. 상단의 텍스트 기능을 이용하여 흰 영역 아무 곳에다가 글자 입력
#   - 입력 글자 : "참 잘했어요" 
text_label = pyautogui.locateOnScreen("text_label.png")
if text_label:
    pyautogui.click(text_label, duration=0.5)
else:
    print("찾기 실패")
    sys.exit()

pyautogui.sleep(2)

# 흰 영역 클릭
# pyautogui.moveTo(600, 600)
pyautogui.click(600, 600)

def my_write(text):
    pyperclip.copy(text)
    pyautogui.hotkey("ctrl", "v")

# pyperclip.copy("참 잘했어요")
# pyautogui.hotkey("ctrl", "v")

my_write("참 잘했어요")

# 3. 5초 대기 후 그림판 종료
#   이 때, 저장하지 않음을 자동을 선택하여 프로그램이 완전 종료되도록 함
pyautogui.sleep(5)

# pyautogui.hotkey("alt", "F4")
# pyautogui.sleep(1)
# pyautogui.hotkey("n")

window.close()
pyautogui.sleep(0.5)
pyautogui.press("n")    # 저장하지 않음