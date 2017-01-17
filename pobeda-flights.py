# By Kirill Snezhko

import requests
from bs4 import BeautifulSoup 
import datetime
import re
import smtplib

# Airport             Code
# Barcelona           GRO
# Wien                XWC
# Cologne             CGN
# Larnaca             LCA
# Milan - Bergamo     BGY
# Milan - Centrum     XIK
# Munich - Memmingen  FMM
# Munixh - Zentrum    ZMU
# Piza                PSA
# Firenze             ZMS
# Zurich              ZLP


desired_home = 'VKO'
desired_destination = 'CGN'
desired_destinations = ['GRO', 'XWC', 'CGN', 'LCA', 'BGY', 'XIK', 
                        'FMM', 'ZMU', 'PSA', 'ZMS', 'ZLP']
desired_minimum_length = 2
desired_maximum_price = 3000

r = requests.post('https://www.pobeda.aero/en/information/book/search_cheap_tickets', 
                  data = {'search_tickets':'1',
                         'city_code_from':desired_home,
                         'city_code_to': desired_destination,
                         'date_departure_from':'10/01/2017',
                         'date_departure_to':'10/03/2017',
                         'is-return': 'no',
                         'date_return_from':'10/01/2017',
                         'date_return_to':'10/03/2017',
                         'max_price':'10000'
                         })

soup = BeautifulSoup(r.text, 'html.parser')
for tag in soup.find_all('br'):
    tag.replaceWith('')
    
string_price = soup.find("div", {"class": "airtickets-cost"}).text.strip(' \t\n\r')
string_dates = soup.find("div", {"class": "airtickets-date"}).text.strip(' \t\n\r')
link = soup.find("a", href=True)['href']

price = int(re.sub("[^0-9]", "", string_price))

string_departure_date, string_arrival_date = string_dates.split('/')
departue_date = datetime.datetime.strptime(string_departure_date, "%d %b %Y ").date()
arrival_date = datetime.datetime.strptime(string_arrival_date, " %d %b %Y").date()

email_text = "Рейс найден!\n" \
             "Из {} в {}, туда {}, обратно {} за {} руб.\n" \
             "КУПИТЬ: {}."

email_text = email_text.format(desired_home, 
                               desired_destination,
                               departue_date.strftime("%Y-%m-%d"),
                               arrival_date.strftime("%Y-%m-%d"),
                               price,
                               link)

print (email_text)

if ((arrival_date - departue_date).days > desired_minimum_length and price < desired_maximum_price):
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.login("YOUR_MAIL", "YOUR_PASS")  
    server_ssl.sendmail("FROM", "FROM", 'Subject: %s\n\n%s' % ("НОВЫЙ РЕЙС!!!", email_text))
    server_ssl.close()