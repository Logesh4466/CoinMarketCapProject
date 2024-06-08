import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

class CoinMarketCapScraper:
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape_coin_data(self, coin):
        url = f"https://coinmarketcap.com/currencies/{coin}/"
        self.driver.get(url)
        data = {}

        # Scrape the data using selenium
        try:
            data['price'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/span').text
            data['price_change'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-overview"]/div[2]/div/div/p').text
            data['market_cap'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[1]/dd').text
            data['market_cap_rank'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[1]/div[2]/div/span').text
            data['volume'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[1]/dd').text
            data['volume_rank'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[2]/div[2]/div/span').text
            data['volume_change'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[3]/div/dd').text
            data['circulating_supply'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[4]/div[1]/dd').text
            data['total_supply'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[5]/div/dd').text
            data['diluted_market_cap'] = self.driver.find_element(By.XPATH, '//*[@id="section-coin-stats"]/div/dl/div[7]/div/dd').text

            # Scraping contracts and social links
            data['contracts'] = []
            data['official_links'] = []
            data['socials'] = []

            # Example of scraping multiple elements
            contracts = self.driver.find_elements(By.XPATH, '//div[contains(text(),"Contracts")]/following-sibling::div//a')
            for contract in contracts:
                data['contracts'].append({
                    'name': contract.text,
                    'address': contract.get_attribute('href')
                })
        except Exception as e:
            data['error'] = str(e)

        return data
    
    def scrape_and_export_to_excel(self, coin, filename):
        data = self.scrape_coin_data(coin)
        df = pd.DataFrame([data])  # Convert the scraped data to a DataFrame
        df.to_excel(filename, index=False)

    def close(self):
        self.driver.quit()
