from beer_search.models import BeerType
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import date
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

    def construct_message(self, beer_type):
        """

        Returns a tweetable message about the given beer type
        """
        if beer_type.available:
            message = "{0} er nýr í Vínbúðinni.".format(beer_type.name)
        else:
            message = "{0} er ekki lengur í Vínbúðinni.".format(beer_type.name)
        return message[:140]

    def handle(self, *args, **options):
        """

        Sends tweets about all beer types marked as being in need of announcement
        """
        beer_types = BeerType.objects.filter(
            needs_announcement=True
        ).all()
        tweepy_api_handle = self.setup_tweepy()
        for beer_type in beer_types:
            message = self.construct_message(beer_type)
            self.tweet(message, tweepy_api_handle)
            beer_type.needs_announcement = False
            beer_type.save()
