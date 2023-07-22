import os
import pyautogui

# 스크린 샷 찍기
# img = pyautogui.screenshot()
# img.save(os.path.join(os.path.dirname(__file__), "screenshot.png"))

# pyautogui.mouseInfo()
# 1401,29 35,104,151 #236897

pixel = pyautogui.pixel(1401, 29)
print(pixel)

# print(pyautogui.pixelMatchesColor(1401, 29, (36, 105, 152)))
# print(pyautogui.pixelMatchesColor(1401, 29, pixel))
print(pyautogui.pixelMatchesColor(1401, 29, (36, 105, 151)))
