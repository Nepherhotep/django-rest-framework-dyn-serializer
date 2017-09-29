from datetime import date
from pprint import pprint

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from test_samples.sample.sampleapp.models import Author, Article, Review


class MainTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.reviewer = get_user_model().objects.create(
            username='reviewer', first_name='reviewer', last_name='reviewer')

        self.author1 = Author.objects.create(name='author 1',
                                             birth_date=date(1985, 1, 31))

        self.author2 = Author.objects.create(name='author 2',
                                             birth_date=date(1986, 2, 20))

        self.articles = []

        for i in range(5):
            for author in [self.author1, self.author2]:
                article = Article.objects.create(title='article {} by {}'.format(i, author.name),
                                                 content='article content {}'.format(i),
                                                 author=author)
                self.articles.append(article)

                for j in range(2, 5):
                    Review.objects.create(article=article,
                                          summary='summary {}'.format(j),
                                          content='content {}'.format(j),
                                          stars=j,
                                          user=self.reviewer)

    def test_list_articles(self):
        response = self.client.get('/article/')

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert len(response_json) == 10, response_json
        assert 'id' in response_json[0], response_json
        assert 'title' not in response_json[0], response_json
        assert 'content' not in response_json[0], response_json

    def test_list_articles_with_title(self):
        response = self.client.get('/article/?article_fields=id,title')

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert len(response_json) == 10, response_json
        assert 'id' in response_json[0], response_json
        assert 'title' in response_json[0], response_json
        assert 'content' not in response_json[0], response_json

    def test_list_articles_with_title_and_content(self):
        response = self.client.get('/article/?article_fields=id,title,content')

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert len(response_json) == 10, response_json
        assert 'id' in response_json[0], response_json
        assert 'title' in response_json[0], response_json
        assert 'content' in response_json[0], response_json

    def test_list_articles_with_author(self):
        response = self.client.get('/article/?article_fields=id,author')

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert 'author' in response_json[0], response_json

        author = response_json[0]['author']

        assert 'id' in author, author
        assert 'name' not in author, author
        assert 'birth_date' not in author, author

    def test_list_articles_with_author_extended_fields(self):
        query = '/article/?article_fields=id,author&author_fields=id,name,birth_date'
        response = self.client.get(query)

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert 'author' in response_json[0], response_json

        author = response_json[0]['author']

        assert 'id' in author, author
        assert 'name' in author, author
        assert 'birth_date' in author, author

    def test_get_article_with_extended_fields(self):
        url = '/article/{}/'.format(self.articles[0].id)
        query = 'article_fields=id,author&author_fields=id,name,birth_date'

        response = self.client.get('{}?{}'.format(url, query))

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert 'author' in response_json, response_json

        author = response_json['author']
        expected_author = {
            'id': self.author1.id,
            'name': 'author 1',
            'birth_date': '1985-01-31'
        }
        assert author == expected_author, author

    def test_limit_fields_as_serializer_meta_attribute(self):
        url = '/article_limit_fields/{}/'.format(self.articles[0].id)
        query = 'article_fields=id,author&author_fields=id,name'

        response = self.client.get('{}?{}'.format(url, query))

        assert response.status_code == 200, response.status_code

        response_json = response.json()
        assert 'author' in response_json, response_json
        assert 'content' not in response_json, response_json

        author = response_json['author']
        expected_author = {
            'id': self.author1.id,
            'name': 'author 1',
        }
        assert author == expected_author, author

    def test_limit_fields_for_nested_serializers_with_many_true(self):
        url = '/author/{}/'.format(self.articles[0].id)
        query = 'author_fields=id,article&article_fields=id,review&review_fields=id,stars'

        response = self.client.get('{}?{}'.format(url, query))

        assert response.status_code == 200, response.status_code

        response_json = response.json()

        assert 'article' in response_json, response_json
        for article in response_json['article']:
            assert 'title' not in article, article
            assert 'review' in article
            for review in article['review']:
                assert 'summary' not in review
                assert 'stars' in review

    def test_list_reviews_with_restricted_fields(self):
        review = Review.objects.first()

        url = '/review/{}/'.format(review.id)
        query = 'review_fields=id,stars,user&user_fields=username,first_name'

        response = self.client.get('{}?{}'.format(url, query))

        assert response.status_code == 200, response.status_code

        response_json = response.json()

        assert 'user' in response_json, response_json
        assert 'first_name' in response_json['user']
        assert 'username' not in response_json['user']
