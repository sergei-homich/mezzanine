from __future__ import print_function, unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand
from django import db

from mezzanine.twitter.models import Query, TwitterQueryException


class Command(BaseCommand):
    """
    Polls the Twitter API for tweets associated to the queries in templates.
    """

    option_list = BaseCommand.option_list + (
        make_option("--force", default=False, action="store_true"),
    )

    def handle(self, **options):
        queries = Query.objects.all()
        if not options["force"]:
            queries = queries.filter(interested=True)
        for query in queries:
            try:
                query.run()
            except TwitterQueryException as e:
                print("Twitter query error [%s]: %s" % (query, e))
        try:
            db.close_connection()
        except:
            pass
