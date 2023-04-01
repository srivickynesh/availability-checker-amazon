import os
import re
import requests
from bs4 import BeautifulSoup
import smtplib
from fake_useragent import UserAgent

def send_mail(URL, sender_email, password, receivers_email, Price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()

    server.login(sender_email, password)
    subject = 'Price fell down!'
    body = 'Check the amazon link ' + URL
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(sender_email, receivers_email, msg)

    print('email has been sent')
    server.quit()

def information(soup, URL, sender_email, password, recievers_email, Price):

    try:
        title_h1 = soup.find("h1")
        title = title_h1.find("span").getText().strip()
        print("\nProduct\t:\n\t", title, "\n")
    except AttributeError:
        print("Product title not found")

    try:
        title = soup.select_one("h1 > span").getText().strip()
        print("\nProduct\t:\n\t", title, "\n")
    except AttributeError:
        print("Product title not found")
        return

    try:
        price = soup.find("span", {"id": "priceblock_ourprice"}).get_text().replace(
            ',', '').replace('₹', '').replace(' ', '').strip()
        print("Current price\t:\t", price)
    except AttributeError:
        print("Product price not found")
        return

    print("Price you expect\t:\t", Price)
    if (float(price) < float(Price)):
        print("YEAH price has fallen!! email will be sent")
        send_mail(URL, sender_email, password, recievers_email, Price)
    else:
        print("seems like you have to wait -) ")

def entry():
    URL = os.environ["URL"]
    Headers = os.environ["HEADERS"]
    Price1 = os.environ["PRICE1"]
    sender_email = os.environ["SENDER_EMAIL"]
    password = os.environ["SENDER_PASSWORD"]
    receivers_email = os.environ["RECEIVER_EMAIL"]

    headers = {"User-Agent": Headers}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    Price = Price1.replace(',', '').replace(' ', '').strip()

    try:
        print("# enable --allow less secured apps-- on your gmail if you want to receive an email")
        information(soup, URL, sender_email, password, receivers_email, Price)
    except AttributeError:
        print("product info not found")

if __name__ == "__main__":
    entry()
