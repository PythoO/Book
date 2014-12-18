import requests
import simplejson as json


class GoogleApi():
    isbn = ''
    title = ''
    description = ''
    authors = ''
    google_url = 'https://www.googleapis.com/books/v1/volumes?q=%s+isbn'

    def __init__(self, isbn):
        self.isbn = isbn

    def get_data(self):
        self.google_url = self.google_url % self.isbn
        response = requests.get(self.google_url)
        html = response.text
        try:
            data = json.loads(html)
        except Exception as e:
            return e.message

        self.title = data['items'][0][u'volumeInfo'][u'title']
        self.authors = ''
        try:
            authors = data['items'][0][u'volumeInfo'][u'authors']
            for auth in authors:
                self.authors += auth + ', '
        except KeyError:
            pass
