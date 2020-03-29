from base import Base
from sqlalchemy import Column, String, Integer, Date, Boolean, Numeric, ForeignKey, UniqueConstraint, PrimaryKeyConstraint


class SituationReport(Base):
    __tablename__ = 'situation_report_data'

    country = Column('country', String(128))
    cases = Column('cases', Integer)
    new_cases = Column('new_cases', Integer)
    deaths = Column('deaths', Integer)
    new_deaths = Column('new_deaths', Integer)
    report_date = Column('report_date', Date)

    __table_args__ = (
        UniqueConstraint('country', 'cases', 'new_cases', 'deaths',
                         'new_deaths', 'report_date', name='_data_unique'),
        PrimaryKeyConstraint('country', 'cases', 'new_cases',
                             'deaths', 'new_deaths', 'report_date'),
    )

    def __init__(self, country, cases, new_cases, deaths, new_deaths, report_date):
        self.country = country
        self.cases = cases
        self.new_cases = new_cases
        self.deaths = deaths
        self.new_deaths = new_deaths
        self.report_date = report_date
