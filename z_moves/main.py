from bs4 import BeautifulSoup
import urllib.request

# Url for each group
groupUrl = 'http://rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g='

source = urllib.request.urlopen(groupUrl).read()

# Entire schedule page object for some group
soup = BeautifulSoup(source, 'lxml')

print(soup.prettify())
# TODO Page parsing

