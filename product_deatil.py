import json
import requests
from bs4 import BeautifulSoup
import random
import time

'output.json'


def save_data_to_file(data, output_path='output.json'):
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    print(f"Data saved to {output_path}")

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x32) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/533.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/608.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.4) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/603.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 11; SM-A205U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.82 Mobile Safari/537.36"
]

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "DNT": "1"
    }

def parser(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    
    categ_tag = soup.select('ol li span[itemprop="name"]')
    if categ_tag:
        category_detail = ' > '.join([cat.get_text(strip=True) for cat in categ_tag])
    else:
        category_detail = "No category_detail available"


    code = soup.select_one('span[itemprop="sku"]')
    code = code.text if code else "No code available"

    name = soup.select_one('h1[itemprop="name"]')
    name = name.text if name else "No name available"

    price = soup.select_one('div.current-price span[itemprop="price"]')
    price = price.text if price else "No data available"

    description = soup.find('div',class_='tab-content')
    description = description.get_text(strip=True) if description else "No description available"

    iamge_tags = soup.select('li.thumb-container img.thumb.js-thumb')
    images = [img['data-image-large-src'] for img in iamge_tags] if iamge_tags else "No image available"

    features = {}

    for dt, dd in zip(soup.select('dl.data-sheet dt.name'), soup.select('dl.data-sheet dd.value')):

        feature_name = dt.get_text(strip=True)
        feature_value = dd.get_text(strip=True)
        features[feature_name] = feature_value
    
    return({
        'link': response.url,
        'product_category':category_detail,
        "product_code": code,
        'name': name,
        'price': price,
        'description': description,
        'images': images,
        'features': features

    })


with open('product_links.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


req = 1

for category,category_data in data.items():
    product_links = category_data['product_links']

    products_details = []

    for product_link in product_links:
        
        headers = get_headers()
        response = requests.get(product_link,headers=headers)
        print(f'Working on {product_link}, you have sent {req} req so far')
        req+=1

        parsed_data = parser(response)
        products_details.append(parsed_data)

        sleep_time = float(format(random.uniform(0.01, 1), ".2f"))
        time.sleep(sleep_time)

    category_data['product_links'] = products_details

    save_data_to_file(data,output_path)
    time.sleep(5)
    print('Going to next category links')

print(f"Final scraped data saved to {output_path}")


