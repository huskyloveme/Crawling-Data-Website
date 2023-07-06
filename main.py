from bs4 import BeautifulSoup
from data_construction import Expectation_Data
import requests as res
import csv
import threading
import time

def write_data_to_file(data_row):
    with open('data_craw_one_thread.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(data_row)

def write_log_fail_to_file(log_text):
    with open('log.txt', 'a', encoding='utf-8') as file_log:
        file_log.write(log_text + '\n')

def process_scraping_data(from_ , to_):
    for i in range(from_, to_ + 1):
        URL_CRAW = "https://www.newegg.com/GPUs-Video-Graphics-Cards/SubCategory/ID-48/Page-" + str(i)
        reponse = res.get(URL_CRAW)
        soup = BeautifulSoup(reponse.text, features="html.parser")

        # Check "Are you a human?" problem
        all_product_in_page = soup.find_all("div", class_="item-cell")
        if not all_product_in_page:
            print("Are you a human?")
        for product_tags in all_product_in_page:
            DATA_RESULT = Expectation_Data.copy()
            try:
                # ItemID and Product Information
                item_ID_tag = product_tags.find("ul", class_="item-features")
                li_tags = item_ID_tag.find_all("li")
                for tags in li_tags:
                    text_li = tags.find("strong").text.strip()
                    if text_li == 'Item #:':
                        DATA_RESULT['itemID'] = str(tags.text).split(':')[1].strip()
                        continue
                    if text_li == 'Model #:':
                        DATA_RESULT['product_information']['model'] = str(tags.text).split(':')[1].strip()
                        continue
                    if text_li == 'DisplayPort:':
                        DATA_RESULT['product_information']['displayport'] = str(tags.text).split(':')[1].strip()
                        continue
                    if text_li == 'Max Resolution:':
                        DATA_RESULT['product_information']['max_resolution'] = str(tags.text).split(':')[1].strip()
                        continue
                    if text_li == 'DirectX:':
                        DATA_RESULT['product_information']['directx'] = str(tags.text).split(':')[1].strip()
                        continue
                    if text_li == 'HDMI:':
                        DATA_RESULT['product_information']['hdmi'] = str(tags.text).split(':')[1].strip()
                        continue

                # Title
                title_tag = product_tags.find("a", class_="item-title")
                if title_tag:
                    DATA_RESULT['title'] = title_tag.text

                # Branding
                branding_tag = product_tags.find("a", class_="item-brand")
                branding_img = branding_tag.find("img")
                if branding_img:
                    DATA_RESULT['branding'] = branding_img['title']

                # Rating and Count Rating
                rating_i = product_tags.find("i", class_ = "rating")
                if rating_i:
                    DATA_RESULT['rating'] = rating_i["aria-label"]
                count_rating_i = product_tags.find("span", class_ = "item-rating-num")
                if count_rating_i:
                    DATA_RESULT['count_rating'] = int(str(count_rating_i.text).strip("()"))

                # Current_price
                current_price_li = product_tags.find("li", class_="price-current")
                if current_price_li:
                    # label_price = str(current_price_li.text)[0]
                    integer_price = current_price_li.find("strong").text
                    decimal_price = current_price_li.find("sup").text
                    DATA_RESULT['current_price'] = str(integer_price) + str(decimal_price)

                #Shipping
                shipping_price_li = product_tags.find("li", class_="price-ship")
                if shipping_price_li:
                    DATA_RESULT['shipping'] = shipping_price_li.text

                # Image_URL
                image_container_a = product_tags.find("a", class_ = "item-img")
                if image_container_a:
                    image_img = image_container_a.find("img")
                    DATA_RESULT['image_url'] = image_img['src']

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
                print("PAGE({}) | {}".format(i, DATA_RESULT['itemID']))
                write_data_to_file(data_list)

            except Exception as e:
                print(e)
                anchor_tags = product_tags.find_all("a", class_="item-img")
                url_fail = anchor_tags[0]["href"]
                print("CAN NOT REQUEST TO URL PRODUCT: {}".format(url_fail))
                write_log_fail_to_file("CAN NOT REQUEST TO URL PRODUCT: {}".format(url_fail))
        time.sleep(1)

def create_thread(from_, to_):
    print("Processing Craw DATA from PAGE({}) -> PAGE({})".format(from_,to_))
    process_scaping_data(from_, to_)

if __name__ == "__main__":

    # # Create Multi thread
    # thread_1 = threading.Thread(target=create_thread, args=(1, 33))
    # thread_2 = threading.Thread(target=create_thread, args=(34, 66))
    # thread_3 = threading.Thread(target=create_thread, args=(67, 100))
    #
    #
    # # Start Multi thread
    # thread_1.start()
    # thread_2.start()
    # thread_3.start()

    #One thread
    process_scaping_data(1, 100)







