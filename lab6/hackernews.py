from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier as Classifier


@route("/")
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    label = request.query.label
    row_id = request.query.id
    row = s.query(News).filter(News.id == row_id)
    row.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/", 34)
    for n in news:
        row = News(title=n["title"],
                   author=n["author"],
                   url=n["url"],
                   comments=n["comments"],
                   points=n["points"])
        if s.query(News).filter(News.title == row.title and News.author == row.author).all():
            continue
        s.add(row)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


if __name__ == "__main__":
    run(host="localhost", port=8080)

