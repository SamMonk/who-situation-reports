import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup

response = requests.get('https://www.who.int/emergencies/diseases/novel-coronavirus-2019/situation-reports/')
soup = BeautifulSoup(response.content, "html.parser")

situation_report_div = soup.find("div", {"id":"PageContent_C006_Col01"})
situation_report_links = situation_report_div.find_all("a")

PDFs = './PDFs/'

for link in situation_report_links:
    filename = os.path.join(PDFs,link['href'].split('/')[-1].split('?')[0])
    if '.pdf' in filename:
        if filename.split('/')[-1] not in os.listdir(PDFs):
            with open(filename, 'wb') as f:
                f.write(requests.get(urljoin("https://www.who.int/",link['href'])).content)
