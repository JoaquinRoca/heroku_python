import os
from flask import Flask,render_template
import psycopg2

app = Flask(__name__, static_folder="static",static_url_path="")

con = psycopg2.connect(
    database="dcq831hkco5on8",
    user="tyderfzsicjagq",
    password="2FyTBBWnZgLDAU_rWICXUk5bDw",
    host="ec2-174-129-26-115.compute-1.amazonaws.com",
    port="5432"
)
cur=con.cursor()

@app.route('/')


def hello():
    picturetoshow="test.png"
    return render_template("presentation.html",pic=picturetoshow)




