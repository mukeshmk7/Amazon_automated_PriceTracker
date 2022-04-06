from urllib import request
import requests
import lxml
import smtplib
from bs4 import BeautifulSoup

with open('user.txt') as f:
    all_text = f.readlines()

url_link = all_text[0].split("=", maxsplit=1)[1].strip()
user_name = all_text[1].split("=", maxsplit=1)[1].strip()
passtext = all_text[2].split("=", maxsplit=1)[1].strip()

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}
response = requests.get(url_link, headers=header).content

soup = BeautifulSoup(response, 'lxml')
price = soup.select_one(selector='span .a-price-whole').getText().replace(".","").replace(',','')
if int(price) < 11000:
    my_email = user_name
    password = passtext
    with smtplib.SMTP("smtp.mail.yahoo.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(
            from_addr=my_email,
            to_addrs=my_email,
            msg=f"Subject:Amazon Price Alert\n\n\nThe product is under sale at {price}\n "
                f"Visit: {url_link}for further info.".encode("utf-8")
        )