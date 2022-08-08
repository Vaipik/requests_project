from bs4 import BeautifulSoup
import csv
import requests
from time import sleep

data = []

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0',
}

query = {
    'q': 'французкий бульдог',
    'page': 1,
}
url = 'https://www.olx.ua/d/uk/zhivotnye/sobaki/'
r = requests.get(url, headers=headers, params=query)
bs = BeautifulSoup(r.text, 'html.parser')
pages = len(bs.select('a.css-1mi714g'))  # Кількість сторінок
start_index = 0

for page in range(1, pages + 1):
    sleep(1)
    query['page'] = page
    print(page)
    r = requests.get(url, headers=headers, params=query)
    bs = BeautifulSoup(r.text, 'html.parser')

    dogs = bs.find_all('div', class_='css-u2ayx9')
    """
        Назва оголошення
        Ціна оголошення
    """
    for dog in dogs:

        dog_title = dog.find('h6', class_='css-v3vynn-Text eu5v0x0').get_text()
        if dog.find('p', class_="css-wpfvmn-Text eu5v0x0") is None:  # Якщо ціни немає
            dog_price = 'Без ціни'
        else:
            dog_price = ', '.join([price.replace('грн.', '').strip()
                                   for price in dog.find('p', class_="css-wpfvmn-Text eu5v0x0").strings])

        data.append(
            {
                'Назва оголошення': dog_title,
                'Ціна оголошення, грн.': dog_price,
            }
            )

    dogs = bs.find_all('p', class_='css-p6wsjo-Text eu5v0x0')  # Місце розташування
    for idx, dog in enumerate(dogs, start_index):
        data[idx]['Розташування'] = dog.get_text()

    dogs = bs.find_all('a', class_='css-1bbgabe')
    """
        Посилання на оголошення
    """
    for idx, link in enumerate(dogs, start_index):
        data[idx]['Посилання'] = f"https://olx.ua{link.get('href')}"

    start_index = idx + 1

data = list(filter(lambda dog: 'extended' not in dog['Посилання'], data))
with open('dogs.csv', 'w') as file:

    column_headers = list(data[0].keys())
    writer = csv.DictWriter(file, column_headers)
    writer.writeheader()
    [writer.writerow(item) for item in data]
