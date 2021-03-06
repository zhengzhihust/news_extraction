from flask import Flask, render_template

from database.dbconn import Database

app = Flask(__name__)


@app.route('/')
def employees():
    def db_query():
        db = Database()
        emps = db.list_data()
        return emps

    res = db_query()
    test = 'test'
    return render_template('news_content.html', result=test, content_type='application/json')
