from selenium import webdriver


class WebDriverContext:
    """Контекст для открытия/закрытия браузера через вебдрайвер."""

    def __init__(self, name: str = 'chrome', head: bool = False):
        self.name = str(name).lower()
        self.head = bool(head)

    def __enter__(self):
        """Вход в контекст, ставит драйвер"""
        match self.name:
            case 'firefox':
                from selenium.webdriver.firefox.service import Service
                from selenium.webdriver.firefox.options import Options
                from webdriver_manager.firefox import GeckoDriverManager
                options = Options()
                options.headless = self.head
                options.page_load_strategy = 'eager'
                self.driver = webdriver.Firefox(
                    service=Service(GeckoDriverManager().install()),
                    options=options
                )
            case 'edge':
                from selenium.webdriver.edge.service import Service
                from selenium.webdriver.edge.options import Options
                from webdriver_manager.microsoft import EdgeChromiumDriverManager
                options = Options()
                options.headless = self.head
                options.page_load_strategy = 'eager'
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Edge(
                    service=Service(EdgeChromiumDriverManager().install()),
                    options=options
                )
            case 'chrome' | _:
                from selenium.webdriver.chrome.service import Service
                from selenium.webdriver.chrome.options import Options
                from webdriver_manager.chrome import ChromeDriverManager
                options = Options()
                options.headless = self.head
                options.page_load_strategy = 'eager'
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                self.driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    chrome_options=options
                )
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекста, завершает сессию общения с браузером."""
        self.driver.quit()
        if exc_type is not None:
            print(f"{exc_type}: {exc_val}; Traceback: {exc_val}")
