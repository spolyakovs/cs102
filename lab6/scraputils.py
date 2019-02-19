import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    table = parser.table.find_all("table", {"class": "itemlist"})[0]
    headers = table.find_all("a", {"class": "storylink"})
    infos = table.find_all("td", {"class": "subtext"})
    scores = table.find_all("span", {"class": "score"})
    authors = table.find_all("a", {"class": "hnuser"})
    for i in range(len(headers)):
        title = headers[i].text
        url = headers[i]["href"]
        comments = infos[i].find_all("a")[3].text.split("\xa0")[0]
        try:
            comments = int(comments)
        except ValueError:
            comments = 0
        author = authors[i].text
        points = scores[i].text.split(" ")[0]
        row = {
            "author": author,
            "comments": comments,
            "points": points,
            "title": title,
            "url": url
        }
        news_list.append(row)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.table.find_all("table")[1].find_all("a")[-1]["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == "__main__":
    url = "https://news.ycombinator.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for i in extract_news(soup):
        print(str(i) + "\r\n")
