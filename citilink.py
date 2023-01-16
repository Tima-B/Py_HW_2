from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from datetime import datetime
import re


class Citilink():
    def __init__(self):
        self.urls = ('https://www.citilink.ru/catalog/noutbuki/?view_type=list&f=available.all',)

    def items(self, driver: webdriver.Chrome):
        # driver.implicitly_wait(5)
        for url in self.urls:
            next_page = url

            while next_page:
                driver.get(next_page)
                ActionChains(driver).pause(2).perform()

                for item in driver.find_elements(By.CLASS_NAME, 'ProductCardHorizontal'):
                    head = item.find_element(By.CSS_SELECTOR, '.ProductCardHorizontal__header-block a')
                    prop = item.find_element(By.CLASS_NAME, 'ProductCardHorizontal__properties').text
                    cpu_hhz_p = re.search(r'Процессор.+?ГГц', prop)
                    ram_gb_p = re.search(r'память.+?ГБ', prop)
                    ssd_gb_p = re.search(r'(Диск|Объем).+?ГБ', prop)
                    price_rub = int(item.get_attribute('data-price'))

                    if cpu_hhz_p:
                        cpu_hhz = float(cpu_hhz_p[0].split()[-2])
                    else:
                        cpu_hhz = float(0.0)
                    if ram_gb_p:
                        ram_gb = int(ram_gb_p[0].split()[-2])
                    else:
                        ram_gb = int(0)
                    if ssd_gb_p:
                        ssd_gb = int(ssd_gb_p[0].split()[-2])
                    else:
                        ssd_gb = int(0)
                    rank = float(cpu_hhz*3 + ram_gb*8 + ssd_gb*0.02 - price_rub * 0.002)
                    name = head.text
                    url = head.get_attribute('href')

                    out = {
                        'cpu_hhz': cpu_hhz,
                        'ram_gb': ram_gb,
                        'ssd_gb': ssd_gb,
                        'price_rub': price_rub,
                        'rank': rank,
                        'name': name,
                        'url': url,
                        'visited_at': str(datetime.today())[:19],
                    }
                    yield out

                next_page = driver.find_elements(By.CSS_SELECTOR, 'a.PaginationWidget__arrow_right')
                if next_page:
                    next_page = next_page[0].get_attribute('href')

        return
