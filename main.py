import requests
import smtplib
from bs4 import BeautifulSoup
# import lxml

PRODUCT_URL = "https://www.amazon.de/dp/B07M5HX7VS/ref=twister_B0B7JLYPVY?_encoding=UTF8&th=1&psc=1"
TARGET_PRICE = 50

ACCEPT_LANGUAGE = "en-US,en;q=0.5"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"

EMAIL = ""
EMAIL_PW = ""

# ----------------- scraping price and title ------------------------ #
header = {
    "User-Agent": USER_AGENT,
    "Accept-Language": ACCEPT_LANGUAGE,
}

response = requests.get(url=PRODUCT_URL, headers=header)


soup = BeautifulSoup(response.text, "lxml")

price = soup.select_one(".a-offscreen").getText()
price_without_curr = price.split("€")[0]
price_as_float = float(price_without_curr.replace(",", "."))
print(price_as_float)

product_name = soup.find(name="span", class_="a-size-large product-title-word-break").text.strip()
print(product_name)

message = f"subject: 📲💻🏷️💶 Amazon Item Price Alert for {product_name}!\n{product_name} " \
          f"are currently priced at {price}." \
          f"This is under your set target of {TARGET_PRICE}€\n" \
          f"Get the product under {PRODUCT_URL}."
message = message.encode("utf-8").strip()


# ---------------- mail alert ---------------------- #
if price_as_float < TARGET_PRICE:
    print("item price is lower than target. Sending mail")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_PW)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=message)
