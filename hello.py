import os
from flask import Flask
import psycopg2
import urlparse

app = Flask(__name__)


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

con = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

@app.route('/')
def hello():
    return render_template("presentation.html")