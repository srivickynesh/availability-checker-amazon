import os
import requests
from bs4 import BeautifulSoup
import smtplib
import re
import time

try:
    import requests
    from bs4 import BeautifulSoup
    import smtplib
    import re
except ImportError:
    print('Some modules are not installed! ')
    print("try\t\tpip install requests bs4 smtplib")


# enable "allow less secured apps" on your gmail for receiving emails
def send_mail(URL, sender_email, password, recievers_email, Price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # The client sends this command to the SMTP server to identify itself and initiate the SMTP conversation.
    server.ehlo()
    server.starttls()  # encrypts the connection

    server.login(sender_email, password)
    subject = 'Amazon Item Price fell down!'
    body = 'Check the amazon link ' + URL
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(sender_email, recievers_email, msg)

    print('email has been sent')
    server.quit()


def information(soup, URL, sender_email, password, recievers_email, Price):
    try:
        title = soup.find(id="productTitle").getText().strip()
        print("\nProduct\t:\n\t", title, "\n")
        price = soup.find(id="priceblock_ourprice").get_text().replace(
            ',', '').replace('₹', '').replace(' ', '').strip()

        print("\n Product that you are looking for is", title)
        print("\n Product current price is ", price)
        print("\n We'll Notify if product price falls below", Price)

        if (float(price) < float(Price)):
            print("YEAH price has fallen!! email will be sent")
            send_mail(URL, sender_email, password, recievers_email, Price)
        else:
            print("seems like you have to wait -) ")
    except AttributeError:
        print("product info not found")

def entry(URL, Price, sender_email, password, recievers_email, Headers):

    headers = {"User-Agent": Headers}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    Price = Price.replace(',', '').replace(' ', '').strip()

    try:
        print(
            "# enable --allow less secured apps-- on your gmail if you want to receive an email"
        )
        information(soup, URL, sender_email, password, recievers_email, Price)
    except AttributeError:
        print("product info not found")

if __name__ == "__main__":

    Headers = os.environ["HEADERS"]
    sender_email = os.environ["SENDER_EMAIL"]
    password = os.environ["SENDER_PASSWORD"]

    with open("urls.txt", "r") as file:
        for line in file:
            URL, Price, recievers_email = line.strip().split(",")
            entry(URL, Price, sender_email, password, recievers_email, Headers)
