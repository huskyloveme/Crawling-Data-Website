from bs4 import BeautifulSoup
from data_construction import Expectation_Data
import requests as res
import csv
import threading
import time

fields = [
    'itemID',
    'title',
    'branding',
    'rating',
    'count_rating',
    'current_price',
    'shipping',
    'image_url',
    'max_resolution',
    'displayport',
    'hdmi',
    'directx',
    'model',
]

def write_1_record_to_file(data_row):
    with open('data_craw.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data_row)

def process_scaping_data(from_ , to_):
    for i in range(from_, to_ + 1):
        # Process SOUP on the page (36-40 products on each page)

        URL_CRAW = "https://www.newegg.com/GPUs-Video-Graphics-Cards/SubCategory/ID-48/Page-" + str(i)
        reponse = res.get(URL_CRAW)
        soup = BeautifulSoup(reponse.text, features="html.parser")
        all_product_in_page = soup.find_all("div", class_="item-cell")
        if not all_product_in_page:
            print("Are you a human?")
        for index, value in enumerate(all_product_in_page):
            soup_ = BeautifulSoup(str(value), features="html.parser")
            anchor_tags = soup_.find_all("a", class_="item-img")

            # Take the URL of each product:
            URL_PRODUCT =  anchor_tags[0]["href"]

            # try:
            reponse_product = res.get(URL_PRODUCT)
            soup_product = BeautifulSoup(reponse_product.text, features="html.parser")

            DATA_RESULT = Expectation_Data

            # ItemID
            item_ID_tag = soup_product.find("li", class_="is-current")
            if item_ID_tag:
                DATA_RESULT['itemID'] = item_ID_tag.find('em').text

            # Title
            title_tag = soup_product.find("h1", class_="product-title")
            if title_tag:
                DATA_RESULT['title'] = title_tag.text


            # Branding
            branding_tag = soup_product.find("div", class_="product-view-brand")
            if branding_tag:
                DATA_RESULT['branding'] = branding_tag.find("a")["title"]

            # Rating and Count Rating
            rating_div = soup_product.find("div", class_="product-rating")
            if rating_div:
                rating_i = rating_div.find("i", class_ = "rating-5")
                if rating_i:
                    DATA_RESULT['rating'] = rating_i["title"]

                count_rating_i = rating_div.find("span", class_ = "item-rating-num")
                if count_rating_i:
                    DATA_RESULT['count_rating'] = int(str(count_rating_i.text).strip("()"))

            # Current_price
            current_price_div = soup_product.find("div", class_="product-price")
            if current_price_div:
                current_price_li = current_price_div.find("li", class_="price-current")
                integer_price = current_price_li.find("strong").text
                decimal_price = current_price_li.find("sup").text
                DATA_RESULT['current_price'] = str(integer_price)+str(decimal_price)

            #Shipping
            shipping = 0

            #Image_URL
            image_url = []
            image_container = soup_product.find("div", class_ = "product-view-container")
            if image_container:
                image_url_div = image_container.find_all("img", class_="product-view-img-original")
                for img_ in image_url_div:
                    image_url.append(str(img_["src"]))
                DATA_RESULT['image_url'] = image_url
            # Product Information
            max_resolution = None
            displayport = None
            hdmi = None
            directx = None
            model = None
            product_infor = soup_product.find_all("table", class_ = "table-horizontal")
            for j in product_infor:
                th_tags = j.find_all("th")
                for th in th_tags:

                    # Max Resolution
                    if str(th.text).strip() == "Max Resolution":
                        td = th.find_next_sibling("td")
                        if td:
                            DATA_RESULT['product_information']['max_resolution'] = td.text.strip()
                        continue

                    # DisplayPort
                    if str(th.text).strip() == "DisplayPort":
                        td = th.find_next_sibling("td")
                        if td:
                            DATA_RESULT['product_information']['displayport'] = td.text.strip()
                        continue

                    # HDMI
                    if str(th.text).strip() == "HDMI":
                        td = th.find_next_sibling("td")
                        if td:
                            DATA_RESULT['product_information']['hdmi'] = td.text.strip()
                        continue

                    # DirectX
                    if str(th.text).strip() == "DirectX":
                        td = th.find_next_sibling("td")
                        if td:
                            DATA_RESULT['product_information']['directx'] = td.text.strip()
                        continue

                    # Model
                    if str(th.text).strip() == "Model":
                        td = th.find_next_sibling("td")
                        if td:
                            DATA_RESULT['product_information']['model'] = td.text.strip()
                        continue

            data_list = [
                DATA_RESULT['itemID'],
                DATA_RESULT['title'],
                DATA_RESULT['branding'],
                DATA_RESULT['rating'],
                DATA_RESULT['count_rating'],
                DATA_RESULT['current_price'],
                DATA_RESULT['shipping'],
                DATA_RESULT['image_url'],
                DATA_RESULT['product_information']['max_resolution'],
                DATA_RESULT['product_information']['displayport'],
                DATA_RESULT['product_information']['hdmi'],
                DATA_RESULT['product_information']['directx'],
                DATA_RESULT['product_information']['model'],
            ]
            print(DATA_RESULT['itemID'])
            write_1_record_to_file(data_list)
            time.sleep(1)
            break
        break


def create_thread(from_, to_):
    print("Processing Craw DATA from PAGE({}) -> PAGE({})".format(from_,to_))
    process_scaping_data(from_, to_)


if __name__ == "__main__":

    #Create Multi thread
    # thread_page_1to20 = threading.Thread(target=create_thread, args=(1, 20))
    # thread_page_21to40 = threading.Thread(target=create_thread, args=(21, 40))
    # thread_page_41to60 = threading.Thread(target=create_thread, args=(41, 60))
    # thread_page_61to80 = threading.Thread(target=create_thread, args=(61, 80))
    # thread_page_81to100 = threading.Thread(target=create_thread, args=(81, 100))

    #Start Multi thread
    # thread_page_1to20.start()
    # thread_page_21to40.start()
    # thread_page_41to60.start()
    # thread_page_61to80.start()
    # thread_page_81to100.start()



    process_scaping_data(2,3)







