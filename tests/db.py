# https://koor.fr/Python/CodeSamplesSqlAlchemy/SimpleMapping.wp


import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:bikeeper@10.0.0.24/bikeeper'

# Test if it works
engine = sqlalchemy.create_engine(SQLALCHEMY_DATABASE_URI, echo=True)
print(engine.table_names())


Base = declarative_base()  # Required


# Definition of the Contact class
class Contact(Base):
    __tablename__ = 'T_Contacts'

    id = Column(Integer, primary_key=True)
    firstName = Column(Text)
    lastName = Column(Text)

    def __init__(self, pk=0, fn="John", ln="Doe"):
        self.id = pk
        self.firstName = fn
        self.lastName = ln

    def __str__(self):
        return self.firstName + " " + self.lastName


# The main part
if __name__ == '__main__':


    #engine = create_engine('mysql+mysqldb://<user>:<pwd>@localhost/<yourDB>', echo=False)
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

    print("--- Construct all tables for the database (here just one table) ---")
    Base.metadata.create_all(engine)  # Only for the first time

    print("--- Create three new contacts and push its into the database ---")
    Session = sessionmaker(bind=engine)
    session = Session()

    doe = Contact(1)
    session.add(doe)

    james = Contact(3, "James", "Bond")
    session.add(james)

    jason = Contact(4, "Jason", "Bourne")
    session.add(jason)

    # session.add_all( [ doe, james, jason ] )
    session.commit()

    print("--- First select by primary key ---")
    contact = session.query(Contact).get(3)
    print(contact)

    print("--- Second select by firstName ---")
    searchedContacts = session.query(Contact).filter(Contact.firstName.startswith("Ja"))
    for c in searchedContacts: print(c)

    print("--- Third select all contacts ---")
    agenda = session.query(Contact)  # .filter_by( firstName='James' )
    for c in agenda: print(c)

    print("--- Try to update a specific contact ---")
    contact = session.query(Contact).get(1)
    contact.lastName += "!"
    session.commit()  # Mandatory

    print("--- Try to delete a specific contact ---")
    session.delete(contact)
    session.commit()