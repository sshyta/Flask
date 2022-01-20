from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import json
from flask import Blueprint
from flask_paginate import Pagination
# from bs4 import BeautifulSoup
import pandas as pd
# 'page': '5',



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bred.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    intro = db.Column(db.String(300), nullable=True)
    text = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.idn


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mac = db.Column(db.Integer, primary_key=False)
    fport = db.Column(db.Integer, primary_key=False)
    data = db.Column(db.String, primary_key=False)
    created = db.Column(db.Integer, primary_key=False)

    def __repr__(self):
        return '<Data %r>' % self.idn

# @app.route('/')
#
# def index():
#     return render_template("index.html")



# @app.route('/')
# @app.route('/home')
# def index():
note_lim = 15
offset_lim = 0


@app.route('/')
def index():
    global note_lim
    global offset_lim
    params = {
        'dev_eui': '393935347B386F14',
        'fport': '2',
        'start_date': '2019-4-26',
        'end_date': '2021-11-26',
        'empty': 'false',
        'utc': 'false',
        'limit': note_lim,
        'offset': offset_lim,
        'dir': '--',
    }

    session = requests.Session()
    session.auth = ('Sshyta@mail.ru', 'pass4Sshyta@mail.ru')
    resp = session.get('https://server.air-bit.eu/api/data/', params=params)
    cont = resp.content
    data = json.loads(cont)
    list = data[0]
    data_list = list['data']
    return render_template('list.html', data_list=data_list)




@app.route('/post')
def post():

    global note_lim
    global offset_lim

    note_lim = 15
    offset_lim = offset_lim + 30

    params = {
        'dev_eui': '393935347B386F14',
        'fport': '2',
        'start_date': '2019-4-26',
        'end_date': '2021-11-26',
        'empty': 'false',
        'utc': 'false',
        'limit': note_lim,
        'offset': offset_lim,
        'dir': '--',
    }

    session = requests.Session()
    session.auth = ('Sshyta@mail.ru', 'pass4Sshyta@mail.ru')
    resp = session.get('https://server.air-bit.eu/api/data/', params=params)
    cont = resp.content
    data = json.loads(cont)
    list = data[0]
    data_list = list['data']
    return render_template('list.html', data_list=data_list)


@app.route('/pred')
def pred():

    global note_lim
    global offset_lim

    note_lim = 15
    offset_lim = offset_lim - 30


    params = {
        'dev_eui': '393935347B386F14',
        'fport': '2',
        'start_date': '2019-4-26',
        'end_date': '2021-11-26',
        'empty': 'false',
        'utc': 'false',
        'limit': note_lim,
        'offset': offset_lim,
        'dir': '--',
    }


    session = requests.Session()
    session.auth = ('Sshyta@mail.ru', 'pass4Sshyta@mail.ru')
    resp = session.get('https://server.air-bit.eu/api/data/', params=params)
    cont = resp.content
    data = json.loads(cont)
    list = data[0]
    data_list = list['data']
    return render_template('list.html', data_list=data_list)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts', methods=['GET'], defaults={"page": 1})
@app.route('/posts/<int:page>')
def posts_page(page=1):
    per_page = 1
    articles = Article.query.order_by(Article.date.desc()).paginate(page, per_page, False).items
    return render_template('posts.html', articles=articles)


@app.route('/posts/del<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "При удалении произошла ошибка"


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect ('/posts')
        except:
            return "При написании произошла ошибка"
    else:
        return render_template("create-article.html")






if __name__ == "__main__":
    app.run(debug=True)





