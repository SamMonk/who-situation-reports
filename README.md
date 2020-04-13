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

PDFs = './PDFs/'https://github.com/SamMonk/who-situation-reports
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
import datetimehttps://github.com/SamMonk/who-situation-reports
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
                    print('Short Array')https://github.com/SamMonk/who-situation-reports
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

### Instructions for updating data

Suggest using a python virtual environment to restore the dependencies:

```python
pip install -r requirements.txt
```
Get new data
```python
python ./report_bot.py
```
Translate to JSON
```python
python ./tabula_pdf_to_json.py
```
INSERT
```python
python ./create_and_insert.py
```
Get USA data out of the database and convert to JSON
```python
python ./get_usa_data_db_to_json_copy.py
```
### How can we fully automate

```yml
# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Python application

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v1
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        pip install pytest
        pytest
```


```bash
[ ! -d "who-situation-reports" ] && git clone https://github.com/SamMonk/who-situation-reports
cd who-situation-reports
git pull
echo "PIP UPGRADE"
pip install --user --upgrade pip
echo "PIP INSTALL VIRTUALENV"
pip install virtualenv
virtualenv myenv
echo "ACTIVATE"
source myenv/bin/activate
apt install python3-pip
pip install --user --upgrade pip
which python
which python3
echo "PACKAGES"
pip-3.2 install -r requirements.txt
echo "REPORT BOT"
python3 ./report_bot.py
python3 ./create_and_insert.py
python3 ./get_usa_data_db_to_json_copy.py
```
