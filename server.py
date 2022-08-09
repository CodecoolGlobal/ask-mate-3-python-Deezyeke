from flask import Flask, render_template, request, redirect, url_for
import util
import data_operations
import connection
import os
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('questions_list.html')


if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
    )
