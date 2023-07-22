import os
import time
import keyboard
from PIL import ImageGrab

curr_path = os.path.dirname(__file__)

def screenshot():
    # 2020년 6월 1일 10시 20분 30초 -> _20200601_102030
    curr_time = time.strftime("_%Y%m%d_%H%M%S")
    img = ImageGrab.grab()
    img.save(os.path.join(curr_path, "image{0}.png".format(curr_time)))

keyboard.add_hotkey("ctrl+shift+s", screenshot)   # 사용자가 F9 키를 누르면 스크린 샷 저장

keyboard.wait("esc")    # 사용자가 esc를 누를 때까지 프로그램 수행