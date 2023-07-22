# Quiz) Selenium 을 이용하여 아래 업무를 자동으로 수행하는 프로그램을 작성하시오

# 1. https://www.w3schools.com 접속 (URL은 구글에서 w3schools 검색)
# 2. 화면 중간 LEARN HTML 클릭
# 3. 상단 메뉴 중 HOW TO 클릭
# 4. 좌측 메뉴 중 Contact Form 메뉴 클릭
# 5. 입력란에 아래 값 입력
#   First Name : 나도
#   Last Name : 코딩
#   Country : Canada
#   Subject : 퀴즈 완료하였습니다.
#   # 위 값들은 변수로 미리 지정해두세요.
# 6. 5초 대기 후 Submit 버튼 클릭
# 7. 5초 대기 후 브라우저 종료

import time
from selenium import webdriver

browser = webdriver.Chrome('/Users/joon/git/workspace/chromedriver')
browser.maximize_window()

browser.get('https://www.w3schools.com')

browser.find_element_by_xpath('//*[@id="main"]/div[2]/div/div[1]/a[1]').click()
browser.find_element_by_xpath('//*[@id="topnav"]/div/div/a[10]').click()
browser.find_element_by_link_text('Contact Form').click()

first_name = "나도"
last_name = "코딩"

subject = "퀴즈 완료하였습니다."

elem = browser.find_element_by_xpath('//*[@id="fname"]')
elem.click()
elem.send_keys(first_name)

elem = browser.find_element_by_xpath('//*[@id="lname"]')
elem.click()
elem.send_keys(last_name)

elem = browser.find_element_by_xpath('//*[@id="country"]/option[text()="Canada"]')
elem.click()

elem = browser.find_element_by_xpath('//*[@id="main"]/div[3]/textarea')
elem.click()
elem.send_keys(subject)

time.sleep(5)

browser.find_element_by_xpath('//*[@id="main"]/div[3]/a').click()

time.sleep(5)
browser.quit()