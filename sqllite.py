import sqlite3

class Sqllite():
    def __init__(self, db_name: str = 'notebook_sel.db'):
        self.db_name = str(db_name)
        self.tb_name = 'computers'

    def __enter__(self):
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.con.close()
        if exc_type is not None:
            print(f"{exc_type}: {exc_val}; Traceback: {exc_val}")

    # Создание базы
    def create(self):
        self.cur.execute(f'DROP TABLE IF EXISTS {self.tb_name};')
        self.cur.execute(
            f'CREATE TABLE {self.tb_name} ('
            'id INTEGER PRIMARY KEY AUTOINCREMENT,'
            'url TEXT,'  # ссылка на страницу товара
            'visited_at timestamp,'  # время посещения страницы
            'name TEXT,'  # наименование товара
            'cpu_hhz REAL,'  # частота процессора, ГГЦ
            'ram_gb INTEGER,'  # объем ОЗУ, Гб
            'ssd_gb INTEGER,'  # Объем SSD, Гб
            'price_rub INTEGER,'  # Цена, руб
            'rank REAL'  # вычисляемый рейтинг
            ');'
        )

    # Запись в базу
    def insert(self, data: list[dict]):
        self.cur.executemany(
            f'''
            INSERT INTO {self.tb_name} (url, visited_at, name, cpu_hhz, ram_gb, ssd_gb, price_rub, rank) 
            VALUES (:url, :visited_at, :name, :cpu_hhz, :ram_gb, :ssd_gb, :price_rub, :rank);
            ''',
            data
        )
        self.con.commit()

    # Выборка ТОПов
    def top_list(self, top=3):
        cols = ('url', 'visited_at', 'name', 'cpu_hhz', 'ram_gb', 'ssd_gb', 'price_rub', 'rank')

        res = self.cur.execute(f'''
            SELECT {','.join(cols)}
            FROM {self.tb_name}
            ORDER BY rank DESC
            LIMIT {top}
            ;''')

        out = res.fetchone()
        while out:
            yield dict(zip(cols, out))
            out = res.fetchone()