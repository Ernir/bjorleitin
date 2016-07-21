from beer_search_v2.models import ProductType
from django.core.management.base import BaseCommand
from django.conf import settings
import tweepy


class Command(BaseCommand):
    def setup_tweepy(self):
        """

        Returns a Tweepy API object, using credentials defined in settings.py
        """
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token = settings.TWITTER_ACCESS_TOKEN
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        return api

    def tweet(self, message_body, api_handle):
        """

        Tweets the given message using a Tweepy API handle.
        """
        api_handle.update_status(message_body)
        print("Tweeted the following: {0}".format(message_body))

    def construct_message(self, product_type):
        """

        Returns a tweetable message about the given beer type
        """
        tweet_length = 140
        domain = "http://bjorleit.info"  # No need to get fancy
        url = "{}{}".format(domain, product_type.get_absolute_url())
        if product_type.available:
            body = "{} fannst".format(product_type.alias)[:(tweet_length - len(url) - 1)]
        else:
            body = "{} er ekki lengur á skrá.".format(product_type.alias)[:(tweet_length - len(url) - 1)]
        message = "{}\n{}".format(body, url)
        return message

    def handle(self, *args, **options):
        """

        Sends tweets about all beer types marked as being in need of announcement
        """
        product_types = ProductType.objects.filter(needs_announcement=True).all()
        tweepy_api_handle = self.setup_tweepy()
        for product_type in product_types:
            message = self.construct_message(product_type)
            self.tweet(message, tweepy_api_handle)
            product_type.needs_announcement = False
            product_type.save()
