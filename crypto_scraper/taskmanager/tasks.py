from celery import shared_task
from .scraper import CoinMarketCapScraper
from .models import ScrapeJob, ScrapeResult

@shared_task
def scrape_coin_data_task(job_id, coin):
    scraper = CoinMarketCapScraper()
    data = scraper.scrape_coin_data(coin)
    job = ScrapeJob.objects.get(id=job_id)
    scraper.close()
    
    ScrapeResult.objects.create(
        job=job,
        coin=coin,
        data=data
    )

    return data
