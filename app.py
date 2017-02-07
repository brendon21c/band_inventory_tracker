from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import itertools
from sqlalchemy import func, exists, and_


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

        if not request.form['show'] or not request.form['item'] or not request.form['item_sold']:
            flash('Please enter in all fields.', 'error')

        # This should add a new item to the database but I'm gettting an error of database locked.
        elif request.form['button'] == "Add":

            #Checks to see if the record already exists in the table to prevent duplicate entries.
            exists_query = db.session.query(exists().where(and_(Show.venue_id == request.form['show'], Show.item_id == request.form['item']))).first()

            result = exists_query[0]

            if result == True:

                flash('Duplicate entry, please update instead of add.', 'error')

            else:

                print(exists_query)

                item_id = request.form['item']
                sold = float(request.form['item_sold'])

                query = Item.query.filter_by(id = item_id).all()

                price = 0

                for x in query:

                    price = round(float(x.item_price * sold),2)


                new_item = Show(request.form['show'], request.form['item'], request.form['item_sold'], price)

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
                        price = round(float(y.item_price * sold),2)
                        x.total_sold = price

                        db.session.commit()


            except Exception as e:

                print("Error entering data")
                print(e)




    return render_template('concert_details.html', concerts = Concert.query.all(), items = Item.query.all())


@app.route('/analysis')
def analysis():

    list_options = ["Total sales for show", "Highest Selling Item", "Most Profitable Item"]

    if not request.args.get('query') or not request.args.get('venue_number'):

        return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), concert = Concert.query.all(), shows = Concert.query.all())


    else:

        query = request.args.get('query')
        show =  request.args.get('venue_number')

        if query == "Total sales for show":

            sold = Show.query.filter_by(venue_id = show).all()

            item_table_join = db.session.query(Show, Item).filter(Show.item_id == Item.id).filter(Show.venue_id == show).all()

            for x,y in item_table_join:
                print(x.items_sold)
                print(round(x.total_sold,2))
                print(y.item_type)
                print(y.item_description)

            # item_number = []
            #
            # for x in sold:
            #
            #     item_number.append(x.item_id)


            return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), shows = Concert.query.all(), totals = item_table_join)


        elif query == "Highest Selling Item":

            sold_query = db.session.query(func.max(Show.items_sold).label("max_sold")).first()

            count = sold_query.max_sold # For highest selling item(s)

            item_table_join = db.session.query(Show, Item).filter(Show.item_id == Item.id).filter(Show.items_sold == count).all()

            return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), shows = Concert.query.all(), totals = item_table_join)

        else:

            sold_query = db.session.query(func.max(Show.total_sold)).first()

            count = sold_query[0] # For highest dollar amount

            item_table_join = db.session.query(Show, Item).filter(Show.item_id == Item.id).filter(Show.total_sold == count).all()

            return render_template('analysis.html', data_list = list_options, venues = Concert.query.all(), shows = Concert.query.all(), totals = item_table_join)



if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
