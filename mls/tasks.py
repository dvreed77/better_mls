from celery import group

from workers import *


@celery.task(name='mls.scrape_listings_task')
def scrape_listings_task():
    feeds = run_all_feeds_worker()


    group(run_all_task.s([pk]) for pk in feeds)()
    # chunk(run_all.s(pk) for pk in feeds)()

@celery.task(name='trlabs.inferno.circle_1.run_all_task')
def run_all_task(feedpks):
    run_all_worker(feedpks)
