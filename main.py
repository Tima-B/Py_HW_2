from driver import WebDriverContext
from sqllite import Sqllite
from notik import Notik
from citilink import Citilink

# Параметры
browser = ('chrome', 'firefox', 'edge')[1]  # Выбор браузера
headless = True  # Скрыть окно браузера
max_items = 600 # Размер выборки
top = 5  # Размер ТОП-списка


sites = (Notik(), Citilink())
with Sqllite() as db:
    # Создание БД
    cnt = 0
    data = []
    db.create()
    # Выбор сайта
    for site in sites:
        if cnt >= max_items:
            break
        print('\n' + site.urls[0])
        with WebDriverContext(browser, headless) as driver:
            # Сбор данных
            for item in site.items(driver):
                cnt += 1
                print('>', end='') # индикатор загрузки
                item = dict(item)
                data.append(item)
                if cnt >= max_items:
                    break
                # Сохраняем в базу
                if cnt%100 == 0:
                    print(' ', cnt)
                    db.insert(data)
                    data.clear()
    # сохраняем, если "небобрали" до целой сотни
    print(' ', cnt)
    db.insert(data)
    data.clear()

    # Вывод топ списка
    print(f"\nТОП-{top} самых лучших ноутов по рейтингу:\n")
    for row in db.top_list(top):
        print(
            f"Рейтинг: {int(row['rank'])}\n"
            f"Имя: {row['name']}\n"
            f"Процессор: {row['cpu_hhz']} ГГц; Память: {row['ram_gb']} ГБ; Диск: {row['ssd_gb']} ГБ\n"
            f"Цена: {row['price_rub']} р.; Дата: {row['visited_at']}\n"
            f"Ссылка: {row['url']}\n"
        )
