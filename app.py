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
            print('update button works')

    return render_template('concert_details.html', concerts = Concert.query.all(), items = Item.query.all())







if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
