import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="function")
def driver():
    service = Service()  # Используем системный geckodriver
    
    options = webdriver.FirefoxOptions()
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")
    
    driver = webdriver.Firefox(service=service, options=options)
    
    driver.get("https://qa-scooter.praktikum-services.ru/")
    
    # Закрываем куки баннер если он есть
    try:
        cookie_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "rcc-confirm-button"))
        )
        cookie_button.click()
    except:
        pass
    
    yield driver
    driver.quit()