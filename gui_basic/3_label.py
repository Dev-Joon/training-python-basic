from tkinter import *
import os

def resource_path(realtive_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        
    return os.path.join(base_path, realtive_path)

root = Tk()
root.title("Nado GUI")
root.geometry("640x480") # 가로 * 세로

label1 = Label(root, text="안녕하세요")
label1.pack()

file_path = os.path.dirname(__file__)
photo = PhotoImage(file=os.path.join(file_path, "img.png"))
label2 = Label(root, image=photo)
label2.pack()

def change():
    label1.config(text="또 만나요")

    global photo2
    photo2 = PhotoImage(file=os.path.join(file_path, "img2.png"))
    label2.config(image=photo2)

btn = Button(root, text="클릭", command=change)
btn.pack()

root.mainloop()

