from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from band_db_manager import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merch_sales.sqlite3'
app.config['SECRET_KEY'] = "RockRules"

db = SQLAlchemy(app)
