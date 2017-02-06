from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


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

            print('add button works')

            new_item = Show(request.form['show'], request.form['item'], request.form['item_sold'])
            #
            db.session.add(new_item)
            db.session.commit()
            #return redirect(url_for('concert_details'))

        else:

            try:

                venue = request.form['show']
                item_id = request.form['item']
                sold = request.form['item_sold']

                # print(venue)
                # print(item_id)
                # print(sold)
                #
                # update = Show.query.filter_by(venue_id = venue).filter_by(item_id = item_id).all()
                #
                # max_query = db.session.query(db.func.max(Show.items_sold)).scalar()
                # print (max_query)
                #
                # item_query = Show.query.filter_by(items_sold = max_query).all()
                #
                # for x, y in item_query:
                #
                #
                #     print(x.item_id, )



                # loops over the query and modifies the item sold count.
                for x in update:

                    x.items_sold = sold
                    db.session.commit()


            except Exception as e:

                print("Error entering data")
                print(e)




    return render_template('concert_details.html', concerts = Concert.query.all(), items = Item.query.all())


@app.route('/analysis')
def analysis():

    list_options = ["test1", "test2", "test3"]

    if not request.args.get('query'):

        return render_template('analysis.html', data_list = list_options, concert = Concert.query.all(), shows = Concert.query.all())


    else:

        query = request.args.get('query')
        show =  request.args.get('show')

        answer = "full house"
        return render_template('analysis.html', data_list = list_options, test_answer = answer)




if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
