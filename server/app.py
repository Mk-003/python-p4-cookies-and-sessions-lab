#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)


app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():

    articles = [article.to_dict() for article in Article.query.all()]

    response = make_response(
        articles,
        200
    )

    return response

    

@app.route('/articles/<int:id>')
def show_article(id):
    if 'page-views' not in session:
        session['page_views']=0
    else:
        session['page_views'] +=1

    if session['page_views'] > 3:
        response = jsonify({"message": "Maximum pageview limit reached"})
        response.status_code = 401
        return response
    else:
        article_data = {"id": id, "title": "Article Title", "content": "Article Content"}
        return jsonify(article_data)


   

if __name__ == '__main__':
    app.run(port=5555, debug=True)
