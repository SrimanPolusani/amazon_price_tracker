# <------Web Scraping------>
import requests
from bs4 import BeautifulSoup
import re

from smtplib import *
import ssl

# <------Product URLs------>
stickers_url = "https://www.amazon.in/CodersParadise-Sticker-Programmer-Waterproof-Professional/dp/B09N41BPYY/ref=sr_1_2?crid=264T5HF3FIGHS&keywords=coding+stickers&qid=1672487553&refinements=p_72%3A1318476031&rnid=1318475031&sprefix=codin%2Caps%2C219&sr=8-2"
novel_12rules_url = "https://www.amazon.in/12-Rules-Life-Antidote-Chaos/dp/0141988517/ref=sr_1_1?crid=1ZOZ4KQQNOUBL&keywords=12+rules+for+life&qid=1672487190&sprefix=12+rules+for+lif%2Caps%2C212&sr=8-1"
redmi_note_url = 'https://www.amazon.in/Redmi-Phantom-Storage-Display-Included/dp/B09T2WYMX6/ref=sr_1_3?keywords=redmi%2Bnote%2B12&qid=1672487739&s=electronics&sr=1-3&th=1'

# <------Headers------>
BROWSER_HEADERS = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36"
}

# <------Products and Desired Prices Dict------>
desired_prizes = {
    stickers_url: 336,
    novel_12rules_url: 315,
    redmi_note_url: 18_000,
}


# <------Mailman Object------>
class MailMan:
    def __init__(self):
        self.cdc = ssl.create_default_context()
        self.from_email = "fakepsyche@gmail.com"
        self.app_password = "wldd cakd wvke pmsf"

    def send_email(self, message: str, to_email):
        with SMTP_SSL("smtp.gmail.com", port=465, context=self.cdc) as server:
            server.login(self.from_email, self.app_password)
            server.sendmail(self.from_email, to_email, msg=message)


# <------PrizeTracker Object------>
class PrizeTracker:
    def __init__(self, requirements_dict: dict):
        self.product_details = requirements_dict
        self.product_name = ""
        self.clean_prize = ""
        self.desired_prize = 0

    # <------Web Scarping Function------>
    def requests_func(self):
        for url, wanted_rate in self.product_details.items():
            self.desired_prize = wanted_rate
            response = requests.get(url, headers=BROWSER_HEADERS)
            website_html = response.text
            soup = BeautifulSoup(website_html, "html.parser")
            self.product_name = soup.find(id="productTitle").text
            prize_of_product = soup.find(name="span", class_="a-price-whole")
            self.clean_prize = prize_of_product.text.replace(',', '')
            self.clean_prize = re.search(r"\d+",
                                         self.clean_prize)  # extracting numbers from the data collected from website
            self.prize_checking_func()  # triggers prize check and MailMan object if required

    # <------Prize Checking Function------>
    def prize_checking_func(self):
        if int(self.clean_prize[0]) <= self.desired_prize:
            text_message = "The prize of {} is\nJUST {} INR \n\nBEST TIME TO BUY!".format(
                self.product_name.strip(),
                self.clean_prize[0]
            )
            print(text_message)
            mailman = MailMan()
            mailman.send_email(
                message=text_message,
                to_email="srimanappu1@gmail.com"
            )
        else:
            pass


# <------Instance of a PrizeTracing Object------>
prize_checking_bot = PrizeTracker(requirements_dict=desired_prizes)
prize_checking_bot.requests_func()

# THIS CODE SHOULD BE EXECUTED VERY 6 HOURS IN THE CLOUD TO CHECK THE PRIZE
# I USED 'PYTHONANYWHERE' TO RUN IT VERY 6 HOURS
