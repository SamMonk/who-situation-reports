from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///who-coronavirus-situation-report-database.db')
Session = sessionmaker(bind=engine)

import base

import situation_reports

base.Base.metadata.create_all(engine)
