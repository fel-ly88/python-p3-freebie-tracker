#!/usr/bin/env python3

from sqlalchemy import create_engine

from models import Company, Dev

if __name__ == '__main__':
    engine = create_engine('sqlite:///freebies.db')
    import ipdb; ipdb.set_trace()


# Example
dev1 = Dev(name="Ash")
comp1 = Company(name="PokéMart", founding_year=1997)
session.add_all([dev1, comp1])
session.commit()

comp1.give_freebie(dev1, "Poké Ball", 50, session)
dev1.received_one("Poké Ball")  # Should return True


freebie = session.query(Freebie).first()
freebie.print_details()
