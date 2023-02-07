from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import pandas as pd


url = 'https://yandex.ru/maps/213/moscow/category/restaurant/184106394/?ll=37.609409%2C55.752864&sll=37.609409%2C55.752826&z=12'

driver = webdriver.Firefox(executable_path='geckodriver')
driver.get(url)
# time.sleep(2)
SCROLL_PAUSE_TIME = 0.1

# Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")

a = time.time()

while True:
    if time.time() - a > 200:
        break
    driver.execute_script("document.getElementsByClassName('scroll__container')[0].scrollBy(0, 10000);")
    time.sleep(SCROLL_PAUSE_TIME)
time.sleep(5)

co = 0
co1 = 0
full_arr = []
for i in driver.find_elements(By.CLASS_NAME, 'search-snippet-view'):
    co += 1
    try:
        name = i.find_element(By.CLASS_NAME, 'search-business-snippet-view__head').text
        category = i.find_element(By.CLASS_NAME, 'search-business-snippet-view__categories').text

        address = i.find_element(By.CLASS_NAME, 'search-business-snippet-view__address').text

        rating = i.find_element(By.CLASS_NAME, 'business-rating-badge-view__rating').text
        try:
            amount = i.find_element(By.CLASS_NAME, 'business-rating-amount-view').text
        except:
            try:
                amount = i.find_element(By.CLASS_NAME, 'business-rating-with-text-view__count').text.rstrip(')').lstrip('(')
            except:
                amount = None

        mean_price = i.find_element(By.CLASS_NAME, 'search-business-snippet-subtitle-view__title').text
        full_arr.append([name, category, address, rating, amount,  mean_price])
        print([name, category, address, rating, amount,  mean_price])
        co1 += 1
    except Exception as e:
        # print(e)
        pass
print(co, co1)

pd.DataFrame(data=full_arr, columns=['name', 'review_num', 'rating', 'type', 'price', 'reviews']).to_csv('./result_y.csv')
