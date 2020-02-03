import requests
from bs4 import BeautifulSoup
import smtplib
import time

URL = 'https://www.amazon.de/dp/B07CXGF728/ref=cm_gf_aAN_i4_d_p0_c0_qd0____________________GlFMw8hzL7m68jTPwUNi'

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

def check_price():
      try:
            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(page.content, 'html.parser')

            title = soup.find(id="productTitle")

            if title is not None:
                  title = title.get_text()
                  print(title.strip())
            else:
                  print(title)

            price = soup.find(id="priceblock_ourprice").get_text()
            price = price.replace(',', '.')
            converted_price = float(price[0:5])
            print(converted_price)

            if (converted_price > 79.99):
                  send_email()


      except AttributeError as e:
            print(e)

def send_email():
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.ehlo()
      server.starttls()
      server.ehlo()

      server.login('panupong.wong@gmail.com','cggdzywsetkdgwzi')

      tolist = ['panupong.wong@gmail.com','panupong.wong@gmail.com']
      subject = 'Price fell down'
      body = 'Check the amazon link https://www.amazon.de/dp/B07CXGF728/ref=cm_gf_aAN_i4_d_p0_c0_qd0____________________GlFMw8hzL7m68jTPwUNi'

      msg = f'Subject: {subject}\n\n{body}'

      server.sendmail(
            'panupong.wong@gmail.com',
            tolist,
            msg
      )
      print('HEY EMAIL HAS BEEN SENT!')

      server.quit()

#Main start here
while(True):
      check_price()
      time.sleep(60)  #check every minute
