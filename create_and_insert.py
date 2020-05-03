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
    #print(filename)
    with open(os.path.join(JSONs, filename), 'rb') as json_file:
        all_data = json.load(json_file)
        for item in all_data:
            for sub_item in item['data']:
                if len(sub_item) < 5:
                    continue
                try:
                    deaths = 0
                    if(sub_item[4]['text'] == "" and len(sub_item) > 5):
                        deaths = int(sub_item[5]['text'])
                    else:
                        deaths = int(sub_item[4]['text'])

                    session.merge(SituationReport(
                        sub_item[0]['text'], 
                        int(sub_item[1]['text']),
                        int(sub_item[2]['text']), 
                        int(sub_item[3]['text']),
                        deaths,
                        datetime.datetime.strptime(filename.split('-')[0], '%Y%m%d')
                        )
                    )
                except ValueError:
                    print(filename)
                    print(sub_item[0]['text'], 'FAILED')

session.flush()
session.commit()
