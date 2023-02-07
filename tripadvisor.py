from selenium import webdriver
import time
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


options = Options()
# options.headless = True
driver = webdriver.Firefox(executable_path='geckodriver', options=options)
driver.get("https://www.tripadvisor.ru/Restaurants-g298484-Moscow_Central_Russia.html")
# try:
#     myElem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, f'/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[1]/div/div/div[{ 30 }]/span/div[1]/div[2]')))
# except:
#     pass

full_arr = []
curr_page = 1
while True:
    for i in driver.find_elements(By.CLASS_NAME, f'emrzT'):
        try:
            name = i.find_element(By.CLASS_NAME, 'bHGqj').text
            t_and_price = i.find_elements(By.CLASS_NAME, 'bhDlF')[1].find_elements(By.CLASS_NAME, 'XNMDG')
            if len(t_and_price) == 1:
                t = None
                price = t_and_price[0].text
            elif len(t_and_price) == 2:
                t = t_and_price[0].text
                price = t_and_price[1].text
            else:
                t = None
                price = None
            small_text = i.find_elements(By.CLASS_NAME, 'XNMDG')
            review_num = int(''.join(small_text[0].text.split()[:-1]))
            rating = float(i.find_element(By.CLASS_NAME, 'RWYkj').get_attribute('aria-label').split()[0].replace(',', '.'))

            reviews = ', '.join([j.text for j in i.find_elements(By.CLASS_NAME, 'cJMPr')])
            arr = [name, review_num, rating,  t, price, reviews]
            full_arr.append(arr)
        except Exception as e:
            print(e)
            pass
    for i in range(3):
        try:
            driver.find_element(By.XPATH, f"/html/body/div[4]/div[3]/div[2]/div[2]/div[2]/div[2]/div[2]/div/div[6]/div[3]/div[5]/div[2]/div/div/a[{curr_page}]").click()
            break
        except Exception as e:
            print(e)
            time.sleep(3)
            continue

    else:
        break
    # wait until page loads after button click
    time.sleep(2)
    if curr_page != 5:
        curr_page += 1

pd.DataFrame(data=full_arr, columns=['name', 'review_num', 'rating', 'type', 'price', 'reviews']).to_csv('./result.csv')
