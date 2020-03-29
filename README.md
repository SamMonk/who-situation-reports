# Who Caranovirus Situation Reports

This python code will download all the latest situation reports.

This project parses the PDF data into individual json files.

We also have the ability to create a sqlite database.

## Get The PDFs

```python
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
        with open(filename, 'wb') as f:
            f.write(requests.get(urljoin("https://www.who.int/",link['href'])).content)
```
## Convert the PDFs to JSON using Tabula

```python
import os
import tabula

PDFs = './PDFs/'
JSONs = './JSONs/'

for filename in os.listdir(PDFs):
    pdf_filename = os.path.join(PDFs, filename)
    json_filename = os.path.join(JSONs, filename).replace('.pdf', '.json')
    tabula.convert_into(pdf_filename, json_filename,
                        output_format="json", pages="all")
```
## Load SQLite Database

```python
import os
import json
import requests
import datetime
from situation_reports import SituationReport
from base import Base
from monkcodedata import Session, engine
Base.metadata.create_all(engine)

JSONs = './JSONs/'

session = Session()

for filename in os.listdir(JSONs):
    print(filename)
    with open(os.path.join(JSONs, filename), 'rb') as json_file:
        all_data = json.load(json_file)
        for item in all_data:
            for sub_item in item['data']:
                if len(sub_item) < 5:
                    print('Short Array')
                    continue
                try:
                    session.merge(SituationReport(
                        sub_item[0]['text'], 
                        int(sub_item[1]['text']),
                        int(sub_item[2]['text']), 
                        int(sub_item[3]['text']),
                        int(sub_item[4]['text']),
                        datetime.datetime.strptime(filename.split('-')[0], '%Y%m%d')
                        )
                    )
                except ValueError:
                    print(sub_item[0]['text'], 'FAILED')

session.flush()
session.commit()
```