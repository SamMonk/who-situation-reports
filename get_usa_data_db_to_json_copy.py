import sqlalchemy as db
import datetime
import json
import decimal

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
    if isinstance(o, decimal.Decimal):
        return str(o)

engine = db.create_engine('sqlite:///who-coronavirus-situation-report-database.db')
metadata = db.MetaData()
db.Table('situation_report_data', metadata, autoload=True, autoload_with=engine)
table = metadata.tables['situation_report_data']
conn = engine.connect()
select_statement = table.select().where(table.c.country == "United States of\rAmerica")
select_return = conn.execute(select_statement)
data = json.dumps([dict(r) for r in select_return], default=default)
with open('./all_usa_data.json', 'w+') as outfile:
    outfile.write(data)
