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








if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
