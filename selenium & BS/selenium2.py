from selenium import webdriver
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

HOST = 'https://legalbet.ru/match-center/'
driver = webdriver.Firefox()
driver.get(HOST)
try:
    accept_cookies_link = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.ID, "gdrp-button-accept")
        )
    )
    accept_cookies_link.click()
except StaleElementReferenceException:
    pass

while True:
    try:
        more_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "pagination-list-more")
            )
        ).find_element_by_class_name('icon-arrow-down')
        more_btn.click()
    except StaleElementReferenceException:
        # break #remove in prod
        continue
    except TimeoutException:
        break
date_blocks_list = driver.find_elements_by_class_name('matches-table-block')
response_list = []
for date_ in date_blocks_list:
    date = date_.find_element_by_class_name('heading-3').text
    table = date_.find_element_by_tag_name('table')
    type_ = table.find_element_by_class_name('match-th').find_element_by_tag_name('div').text
    time_ = None
    vs = None
    league = None
    bets = []
    for tr in table.find_elements_by_tag_name('tr'):
        if 'league-row' in tr.get_attribute('class'):
            league = tr.find_element_by_class_name('league-td').text
        for td in tr.find_elements_by_tag_name('td'):
            #print(td.text, td.get_attribute('class'))
            if 'match-td' in td.get_attribute('class'):
                time_ = td.find_element_by_class_name('time').text
                vs = td.find_element_by_class_name('link').text.split('—')
            elif 'feeds-td' in td.get_attribute('class'):
                continue
            elif 'odd-td' in td.get_attribute('class'):
                bets.append(td.text)
            if len(bets) == 5:
                response_list.append([date, type_, league, time_, vs[0].strip(), vs[1].strip(), bets])
                with open('bet.csv', 'a') as f:
                    f.write(';'.join([';'.join([i for i in e]) if type(e) is list else e for e in response_list[-1]]))
                    f.write('\n')
                bets = []

# with open('bet.csv', 'w') as f:
#     f.write(';'.join([';'.join([i for i in e]) if type(e) is list else e for e in response_list]))

print('Finaly')
    # except TimeoutException:
    #     time.sleep(5)

