from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ScrapeJob
from .serializers import  ScrapeResultSerializer
from .tasks import scrape_coin_data_task
from .scraper import CoinMarketCapScraper
import pandas as pd
import os

class StartScrapingView(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])
        job = ScrapeJob.objects.create()
        
        for coin in coins:
            scrape_coin_data_task.delay(job.id, coin)
        
        return Response({'job_id': job.id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        try:
            job = ScrapeJob.objects.get(id=job_id)
        except ScrapeJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        results = job.results.all()
        serializer = ScrapeResultSerializer(results, many=True)
        return Response({'job_id': job_id, 'tasks': serializer.data})
    

    def post(self, request, job_id):
        try:
            job = ScrapeJob.objects.get(id=job_id)
        except ScrapeJob.DoesNotExist:
            return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        
        coin = request.data.get('coin')
        filename = 'output.xlsx'  

        # Create an instance of the scraper and call the method to export to Excel
        scraper = CoinMarketCapScraper()
        data = scraper.scrape_coin_data(coin)
        df = pd.DataFrame([data])

        # Ensure directory exists
        directory = 'C:/Users/91763/Desktop/CoinMarketCapProject/crypto_scraper/taskmanager'
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Write the DataFrame to an Excel file
        excel_filepath = os.path.join(directory, filename)
        df.to_excel(excel_filepath, index=False)

        return Response({'excel_filepath': excel_filepath}, status=status.HTTP_200_OK)