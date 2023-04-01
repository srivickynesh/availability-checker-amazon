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
def send_mail(URL, sender_email, password, receivers_email, Price):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # The client sends this command to the SMTP server to identify itself and initiate the SMTP conversation.
    server.ehlo()
    server.starttls()  # encrypts the connection

    server.login(sender_email, password)
    subject = 'Price fell down!'
    body = 'Check the amazon link ' + URL
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(sender_email, receivers_email, msg)

    print('email has been sent')
    server.quit()


def information(soup, URL, sender_email, password, receivers_email, Price):
    try:
        title = soup.find(id="productTitle").getText().strip()
        print("\nProduct\t:\n\t", title, "\n")
        price = soup.find(id="priceblock_ourprice").get_text().replace(
            ',', '').replace('₹', '').replace(' ', '').strip()
        print("Current price\t:\t", price)
        print("Price you expect\t:\t", Price)
        if (float(price) < float(Price)):
            print("YEAH price has fallen!! email will be sent")
            send_mail(URL, sender_email, password, receivers_email, Price)
        else:
            print("seems like you have to wait -) ")
    except AttributeError:
        print("product info not found")


def entry():
    URL = os.environ["URL"]
    Price = os.environ["PRICE1"]
    sender_email = os.environ["SENDER_EMAIL"]
    password = os.environ["SENDER_PASSWORD"]
    receivers_email = os.environ["RECEIVER_EMAIL"]

    Headers = os.environ["HEADERS"]
    headers = {"User-Agent": Headers}

    while True:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        Price = Price.replace(',', '').replace(' ', '').strip()

        try:
            print(
                "# enable --allow less secured apps-- on your gmail if you want to receive an email"
            )
            information(soup, URL, sender_email, password, receivers_email, Price)
        except AttributeError:
            print("product info not found")

        time.sleep(60 * 60 * 3)  # Sleep for 3 hours

if __name__ == "__main__":
    entry()
