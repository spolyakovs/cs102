from bottle import (route, run, template, request, redirect)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from bayes_test import clean


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
    row = s.query(News).filter(News.id == row_id).first()
    row.label = label
    s.commit()
    classifier.fit([clean(row.title).lower()], [label])
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/")
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
    news = s.query(News).filter(News.label == None).all()
    titles = [row.title for row in news]
    labels = classifier.predict(titles)
    print(labels)
    good_rows = []
    maybe_rows = []
    never_rows = []
    for i in range(len(labels)):
        if labels[i] == 'good':
            good_rows.append(news[i])
            print(news[i].title)
        elif labels[i] == 'maybe':
            maybe_rows.append(news[i])
        elif labels[i] == 'never':
            never_rows.append(news[i])
    return template('recommended', good_rows=good_rows, maybe_rows=maybe_rows, never_rows=never_rows)


if __name__ == "__main__":
    s = session()
    classifier = NaiveBayesClassifier()
    tagged_news = s.query(News).filter(News.label != None).all()
    titles = []
    labels = []
    for row in tagged_news:
        titles.append(row.title)
        labels.append(row.label)
    classifier.fit(titles, labels)
    run(host="localhost", port=8080)
