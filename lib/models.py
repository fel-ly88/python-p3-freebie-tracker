from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    founding_year = Column(Integer)

    freebies = relationship("Freebie", backref="company")
    devs = relationship("Dev", secondary="freebies", back_populates="companies")

    @classmethod
    def oldest_company(cls, session):
        return session.query(cls).order_by(cls.founding_year).first()

    def give_freebie(self, dev, item_name, value, session):
        freebie = Freebie(item_name=item_name, value=value, dev=dev, company=self)
        session.add(freebie)
        session.commit()

class Dev(Base):
    __tablename__ = "devs"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    freebies = relationship("Freebie", backref="dev")
    companies = relationship("Company", secondary="freebies", back_populates="devs")

    def received_one(self, item_name):
        return any(f.item_name == item_name for f in self.freebies)

    def give_away(self, other_dev, freebie, session):
        if freebie in self.freebies:
            freebie.dev = other_dev
            session.commit()

class Freebie(Base):
    __tablename__ = "freebies"
    id = Column(Integer, primary_key=True)
    item_name = Column(String)
    value = Column(Integer)
    dev_id = Column(Integer, ForeignKey("devs.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))

    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"