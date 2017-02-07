from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import itertools


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merch_sales.sqlite3'
app.config['SECRET_KEY'] = "RockRules"

db = SQLAlchemy(app)
from models import * # Needs to be after db, otherwise no tables are created.


@app.route('/')
def home_page():


    return render_template('home_page.html', concerts = Concert.query.all())

@app.route('/new_show', methods = ['GET', 'POST'])
def new_show():

    if request.method == 'POST':

        show = Concert(request.form['name'], request.form['date'])

        db.session.add(show)
        db.session.commit()
        return redirect(url_for('new_show'))

    return render_template('new_show.html')

@app.route('/new_item', methods = ['GET', 'POST'])
def new_item():

    if request.method == 'POST':

        item = Item(request.form['type'], request.form['description'], request.form['price'])

        db.session.add(item)
        db.session.commit()
        return redirect(url_for('new_item'))


    return render_template('new_item.html', Items = Item.query.all())


@app.route('/concert_details', methods = ['GET', 'POST'])
def concert_details():

    if request.method == 'POST':

        # This should add a new item to the database but I'm gettting an error of database locked.
        if request.form['button'] == "Add":

            item_id = request.form['item']
            sold = float(request.form['item_sold'])

            query = Item.query.filter_by(id = item_id).all()

            price = 0

            for x in query:

                price = float(x.item_price * sold)


            print(price)

            new_item = Show(request.form['show'], request.form['item'], request.form['item_sold'], price)
            #
            db.session.add(new_item)
            db.session.commit()
            #return redirect(url_for('concert_details'))

        else:

            try:

                venue = request.form['show']
                item_id = request.form['item']
                sold = float(request.form['item_sold'])

                query = Item.query.filter_by(id = item_id).all()

                price = 0

                update = Show.query.filter_by(venue_id = venue).filter_by(item_id = item_id).all()


                # loops over the query and modifies the item sold count.
                for x in update:
                    for y in query:

                        x.items_sold = sold
                        price = float(y.item_price * sold)
                        x.total_sold = price

                        db.session.commit()


            except Exception as e:

                print("Error entering data")
                print(e)




    return render_template('concert_details.html', concerts = Concert.query.all(), items = Item.query.all())


@app.route('/analysis')
def analysis():

    list_options = ["Total sales for show", "Highest Total Selling Item"]

    if not request.args.get('query') or not request.args.get('venue_number'):

        return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), concert = Concert.query.all(), shows = Concert.query.all())


    else:

        query = request.args.get('query')
        show =  request.args.get('venue_number')

        if query == "Total sales for show":

            sold = Show.query.filter_by(venue_id = show).all()

            number_sold = []

            item_number = []

            for x in sold:

                number_sold.append(x.items_sold)

                for y in sold:

                    item_number.append(y.item_id)


            return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), shows = Concert.query.all(), items = Show.query.filter_by(venue_id = show).all(), totals = Show.query.filter_by(venue_id = show).all())


        else:

            answer = "full house"

            return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), shows = Concert.query.all(), test_answer = answer)


def get_price_list(number_of_sold_list):
    pass

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
