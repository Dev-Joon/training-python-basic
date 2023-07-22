import time
from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

browser = webdriver.Chrome('/Users/joon/git/workspace/chromedriver')
browser.maximize_window()
browser.get('https://m-flight.naver.com/')

# 가는 날 클릭
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[2]/button[1]').click()
# browser.find_element_by_link_text('가는 날').click()
time.sleep(5)

browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[6]/td[1]/button/b').click()

# 오는 날 클릭
time.sleep(1)
#browser.find_elements_by_link_text('5')[1].click()
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[10]/div[2]/div[1]/div[2]/div/div[2]/table/tbody/tr[6]/td[2]/button/b').click()

time.sleep(1)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div/div[2]/div[1]/button[2]/i').click()

time.sleep(1)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[10]/div[2]/section/section/button[1]').click()

time.sleep(2)
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[10]/div[2]/section/section/div/button[2]/i[1]').click()

time.sleep(2)
# browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div/button').click()
# browser.find_element_by_link_text('항공권 검색').click()
browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[4]/div/div/button').click()

try:
    elem = WebDriverWait(browser, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div[1]/div[5]/div/div[3]/div[2]/div/button')))    
    print(elem.text)
except:
    print("실패했어요")

# 첫 번째 결과 출력
# elem = browser.find_element_by_xpath('//*[@id="__next"]/div/div[1]/div[5]/div/div[3]/div[2]/div/button')
# print(elem.text) # element 내에 있는 text 부분을 출력

time.sleep(5)


browser.quit()