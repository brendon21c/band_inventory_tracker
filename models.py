from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from app import db


class Concert(db.Model):

    """This table will list concert dates and venue."""

    __tablename__ = 'Concert_List'

    id = db.Column('Venue_ID',db.Integer, primary_key = True)
    date = db.Column(db.String(20))
    venue = db.Column(db.String(50))


    def __init__(self, date, venue):

        self.date = date
        self.venue = venue



class Show(db.Model):

    """ This is the table for the specific show, i.e. merch sold, etc. """

    __tablename__ = 'Concert_Totals'
    id = db.Column('Sales_Item',db.Integer, primary_key = True)
    venue_id = db.Column(db.Integer, ForeignKey('Concert_List.Venue_ID'))
    item_id = db.Column(db.Integer, ForeignKey('Items.Item_ID'))
    items_sold = db.Column(db.Integer)

    def __init__(self, venue_id, item_id, items_sold):

        self.venue_id = venue_id
        self.item_id = item_id
        self. items_sold = items_sold



class Item(db.Model):
    """Table listing all products that can be sold."""

    __tablename__ = 'Items'

    id = db.Column('Item_ID', db.Integer, primary_key = True)
    item_type = db.Column(db.String(20))
    item_description = db.Column(db.String(50))
    item_price = db.Column(db.Float)

    def __init__(self, item_type, item_description, item_price):

        self.item_type = item_type
        self.item_description = item_description
        self.item_price = item_price
