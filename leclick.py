import time

from bs4 import BeautifulSoup
import requests
import pandas as pd

offset = 0

full_arr = []
while True:
    url = f'https://leclick.ru/restaurants/index/offset/{offset}?ajax=1&keyword='
    offset += 12
    page = requests.get(url).json()['restaurants']
    if page == '':
        break
    try:
        soup = BeautifulSoup(page, 'html.parser')
    except Exception as e:
        print(e)
        break

    cards = soup.find_all('div', {'class': 'restCard'})
    for i in cards:
        try:
            title = i.find('div', {'class': 'title'}).text
            price = i.find('div', {'class': 'price'})['title']
            address = i.find('span', {'class': 'address'}).text
            type = i.find_all('span')[-1].text
            arr = [title, price, address, type]
            full_arr.append(arr)
            print(arr)
        except:
            pass

    time.sleep(2)
pd.DataFrame(data=full_arr, columns=['title', 'price', 'address', 'type']).to_csv('./result.csv')
