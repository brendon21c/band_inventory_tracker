from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merch_sales.sqlite3'
app.config['SECRET_KEY'] = "RockRules"

db = SQLAlchemy(app)
from band_db_manager import * # Needs to be after db, otherwise no tables are created.







if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
