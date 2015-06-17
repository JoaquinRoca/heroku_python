
from flask import Flask,render_template
import getdata

app = Flask(__name__, static_folder="static",static_url_path="")


@app.route('/')
def hello():
    return render_template("presentation.html")

getdata.startup()


