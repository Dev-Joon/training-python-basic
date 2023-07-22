from tkinter import *
import os

root = Tk()
root.title("제목 없음 - Windows 메모장")
root.geometry("640x480")

menu = Menu(root)

filepath = os.path.join(os.path.dirname(__file__), "mynote.txt")

def open_file():
    if os.path.isfile(filepath):    # 파일 있으면 True, 없으면 False
        with open(filepath, "r", encoding="utf8") as f:
            txt.delete("1.0", END)  # 텍스트 위젯 본문 삭제
            txt.insert(END, f.read())   # 파일 내용을 본문에 입력

def save_file():
    with open(filepath, "w", encoding="utf8") as f:
        f.write(txt.get("1.0", END))    # 모든 내용을 가져와서 저ㅇ

def exit():
    root.quit()

menu_file = Menu(menu, tearoff=0)
menu_file.add_command(label="새로 만들기(N)")
menu_file.add_command(label="새 창(W)")
menu_file.add_command(label="열기(O)", command=open_file)
menu_file.add_command(label="저장(S)", command=save_file)
menu_file.add_command(label="다른 이름으로 저장(A)")
menu_file.add_separator()
menu_file.add_command(label="페이지 설정(U)")
menu_file.add_command(label="인쇄(P)")
menu_file.add_separator()
menu_file.add_command(label="끝내기(X)", command=exit)
menu.add_cascade(label="파일(F)", menu=menu_file)

# menu_edit = Menu(menu, tearoff=0)
menu.add_cascade(label="편집(E)")

# menu_o = Menu(menu, tearoff=0)
menu.add_cascade(label="서식(O)")

# menu_view = Menu(menu, tearoff=0)
menu.add_cascade(label="보기(V)")

# menu_help = Menu(menu, tearoff=0)
menu.add_cascade(label="도움말(H)")

scrollbar = Scrollbar(root)
scrollbar.pack(side="right", fill="y")

# 본문 영역
txt = Text(root, yscrollcommand=scrollbar.set)
txt.pack(side="left", fill="both", expand=True)

scrollbar.config(command=txt.yview)
root.config(menu=menu)
root.mainloop()