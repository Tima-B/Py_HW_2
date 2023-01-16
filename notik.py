from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime

# Выботка c сайта Notik.ru
class Notik():
    def __init__(self):
        # self.urls = ('file://c:/Www/git/web_scraping/temp_notik.html',)
        self.urls = (
            'https://www.notik.ru/search_catalog/filter/work.htm',
            'https://www.notik.ru/search_catalog/filter/home.htm',
            'https://www.notik.ru/search_catalog/filter/universal.htm',
            'https://www.notik.ru/search_catalog/filter/base.htm',
            'https://www.notik.ru/search_catalog/filter/mobile.htm',
            'https://www.notik.ru/search_catalog/filter/ultrabooks.htm',
            'https://www.notik.ru/search_catalog/filter/ultrabook-transformer.htm',
        )

    def items(self, driver: webdriver.Chrome):

        # Перебор Url-ов
        for url in self.urls:
            driver.get(url)
            ActionChains(driver).pause(2).perform()
            pages = [None]
            paginator = driver.find_elements(By.CLASS_NAME, 'paginator')
            if paginator:
                pages.extend(
                    v.get_attribute('href')
                    for v in paginator[0].find_elements(By.TAG_NAME, 'a')[1:]
                )

            # Перебор страниц
            for page in pages:
                if page is not None:
                    driver.get(page)
                    ActionChains(driver).pause(2).perform()

                # Пеебор товаров на странице
                for item in driver.find_elements(By.CLASS_NAME, 'goods-list-table'):
                    tds = item.find_elements(By.TAG_NAME, 'td')
                    ram_ssd = tds[2].text.split()
                    price_name = tds[7].find_element(By.TAG_NAME, 'a')
                    cpu_hhz = int(tds[1].text.rsplit(None, 2)[-2])/1000
                    ram_gb = int(ram_ssd[0])
                    ssd_gb = int(ram_ssd[-2])
                    price_rub = price_name.get_attribute('ecprice')
                    name = price_name.get_attribute('ecname')
                    url = tds[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
                    rank = cpu_hhz*3 + ram_gb*8 + ssd_gb*0.02 - float(price_rub)*0.002

                    out = {
                        'cpu_hhz': cpu_hhz,
                        'ram_gb': ram_gb,
                        'ssd_gb': ssd_gb,
                        'price_rub': price_rub,
                        'name': name,
                        'url': url,
                        'rank': rank,
                        'visited_at': str(datetime.today())[:19],
                    }
                    yield out

        return
