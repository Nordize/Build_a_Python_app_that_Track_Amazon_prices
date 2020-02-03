import requests
from bs4 import BeautifulSoup
import smtplib
import time
from lxml import html
import re

URL = 'https://www.aliexpress.com/item/32854607161.html?spm=a2g01.11715694.fdpcl001.5.7117aYBFaYBFPZ&gps-id=5547572&scm=1007.19201.130907.0&scm_id=1007.19201.130907.0&scm-url=1007.19201.130907.0&pvid=def5c717-1729-476d-b9f5-b71eedbbf647'

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

def check_price():
      try:
            page = requests.get(URL, headers=headers)

            soup = BeautifulSoup(page.content, 'html.parser')

            title = soup.find("title")

            #print(title)

            tree = html.fromstring(page.content)

            script = tree.xpath('//script[contains(., "GaData")]')[0]
            match = re.findall(r"US \$[^\]]+", script.text)
            print(script.text)

            match_splited = [i.split(",",1)[0] for i in match]
            print(match_splited)

            #display index no of list

            for item in match_splited:
                  print(match_splited.index(item)+1,item)

            product_name = match_splited[1]
            product_price = float(str(match_splited[2][4:]).replace('"',''))   #now is stabling for only $xx.xx price have to re-index for $xxx.xx

            print("Meta Tag NAME is: "+product_name)
            print("Product price is: {}".format(product_price))

            if (product_price < 9.99):  #email triggner condition
                  send_email()



      except AttributeError as e:
            print(e)



def send_email():
      server = smtplib.SMTP('smtp.gmail.com',587)
      server.ehlo()
      server.starttls()
      server.ehlo()

      server.login('panupong.wong@gmail.com','gvbfuelocahlucmf')  #get password from google password API

      tolist = ['panupong.wong@gmail.com','panupong.wong@gmail.com']
      subject = 'Price fell down'
      body = 'Check the Aliexpress link>>>'+URL

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
      time.sleep(60)  #check every minute #number is minute