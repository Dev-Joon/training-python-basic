from imap_tools import MailBox
from account import *

# mailbox = MailBox("imap.gmail.com", 993)
# mailbox.login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder="INBOX")
# mailbox.logout()

with MailBox("imap.gmail.com", 993).login(EMAIL_ADDRESS, EMAIL_PASSWORD, initial_folder="INBOX") as mailbox:
    # for msg in mailbox.fetch():                                   # 전체 메일 다 가져오기
    #     print("[{}] {}".format(msg.from_, msg.subject))
    
    # for msg in mailbox.fetch('(UNSEEN)'):                         # 읽지 않은 메일 가져오기
    #     print("[{}] {}".format(msg.from_, msg.subject))
    
    # for msg in mailbox.fetch('(FROM sshimdy8919@naver.com)'):     # 특정인이 보낸 메일 가져오기
    #     print("[{}] {}".format(msg.from_, msg.subject))
    
    # 작은 따옴표로 먼저 감싸고, 실제 TEXT 부분은 큰 따옴표로 감싸주세요 (띄어쓰기로 구분하여 "test", "mail" 이라는 각각의 단어를 포함하는 메일을 찾게 됩니다)
    # for msg in mailbox.fetch('(TEXT "test mail")'): # 어떤 글자를 포함하는 메일 (제목, 본문)
    #     print("[{}] {}".format(msg.from_, msg.subject))
        
    # for msg in mailbox.fetch('(SUBJECT "test mail")'): # 어떤 글자를 포함하는 메일 (제목만)
    #     print("[{}] {}".format(msg.from_, msg.subject))
    
    # 한글은 제약이 있어서 조건을 통해서 가져온 문구중에서 필터링하는 우회 방식을 사용해야 함
    # for msg in mailbox.fetch(reverse=True): # 어떤 글자(한글)을 포함하는 메일 필터링 (제목만)
    #     if "테스트" in msg.subject :
    #         print("[{}] {}".format(msg.from_, msg.subject))
            
    # for msg in mailbox.fetch('(SENTSINCE 07-Nov-2021)', reverse=True):  # 특정 날자 이후에 온 메일
    #     print("[{}] {}".format(msg.from_, msg.subject))
    
    # for msg in mailbox.fetch('(ON 09-Jan-2022)', reverse=True):           # 특정 날짜에 온 메일
    #     print("[{}] {}".format(msg.from_, msg.subject))
        
    # 2가지 이상의 조건을 모두 만족하는 메일 (그리고 조건)
    # for msg in mailbox.fetch('(ON 09-Jan-2022 SUBJECT "test mail")', reverse=True):
    #     print("[{}] {}".format(msg.from_, msg.subject))
        
    # 2가지 이상의 조건 중 하나라도 만족하는 메일 (또는 조건)
    for msg in mailbox.fetch('(OR ON 09-Jan-2022 SUBJECT "test mail")', reverse=True):
        print("[{}] {}".format(msg.from_, msg.subject))
        
    # imap tools 라고 구글에 치면 쿼리부분에 대한 설명이 자세히 나옴