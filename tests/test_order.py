import pytest
import time
from pages.main_page import MainPage
from pages.order_page import OrderPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestOrder:
    @pytest.mark.parametrize("order_button,test_data", [
        ("top", {
            "first_name": "Иван",
            "last_name": "Петров", 
            "address": "Москва, ул. Ленина, 1",
            "phone": "89991234567",
            "delivery_date": "20.12.2024",
            "rental_period": "сутки",
            "color": "black",
            "comment": "Позвонить за час"
        }),
        ("bottom", {
            "first_name": "Мария",
            "last_name": "Сидорова",
            "address": "Москва, ул. Пушкина, 10", 
            "phone": "89997654321", 
            "delivery_date": "25.12.2024",
            "rental_period": "двое суток",
            "color": "grey",
            "comment": "Оставить у двери"
        })
    ])
    def test_successful_order(self, driver, order_button, test_data):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        try:
            print(f"\n=== НАЧИНАЕМ ТЕСТ ЗАКАЗА ({order_button} кнопка) ===")
            
            # Нажимаем на кнопку заказа
            if order_button == "top":
                print("Кликаем верхнюю кнопку заказа")
                main_page.click_order_button_top()
            else:
                print("Кликаем нижнюю кнопку заказа")
                main_page.click_order_button_bottom()
            
            # Ждем загрузки страницы заказа
            print("Ожидаем загрузки страницы заказа...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(order_page.FIRST_NAME_INPUT)
            )
            print("✓ Страница заказа загружена")
            
            # Заполняем первую страницу заказа
            order_page.fill_first_page(
                test_data["first_name"],
                test_data["last_name"], 
                test_data["address"],
                test_data["phone"]
            )
            
            # Ждем загрузки второй страницы
            print("Ожидаем загрузки второй страницы...")
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(order_page.DELIVERY_DATE_INPUT)
            )
            print("✓ Вторая страница загружена")
            
            # Заполняем вторую страницу заказа
            order_page.fill_second_page(
                test_data["delivery_date"],
                test_data["rental_period"],
                test_data["color"],
                test_data["comment"]
            )
            
            # Подтверждаем заказ
            order_page.confirm_order()
            
            # Проверяем сообщение об успешном заказе
            success_message = order_page.get_success_message()
            assert "Заказ оформлен" in success_message, f"Ожидалось 'Заказ оформлен', но получено: {success_message}"
            
            print("✓ Тест заказа завершен успешно!")
            
        except Exception as e:
            print(f"✗ ОШИБКА: {e}")
            order_page.take_screenshot("final_error")
            raise e

    def test_scooter_logo_redirect(self, driver):
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        
        print("\n=== ТЕСТ РЕДИРЕКТА ПО ЛОГОТИПУ САМОКАТА ===")
        
        # Переходим на страницу заказа
        main_page.click_order_button_top()
        
        # Ждем загрузки страницы заказа
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(order_page.FIRST_NAME_INPUT)
        )
        print("✓ Страница заказа загружена")
        
        # Кликаем на логотип Самоката
        main_page.click_scooter_logo()
        
        # Проверяем, что вернулись на главную страницу
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://qa-scooter.praktikum-services.ru/")
        )
        print("✓ Успешно вернулись на главную страницу")

    def test_yandex_logo_redirect(self, driver):
        main_page = MainPage(driver)
        
        print("\n=== ТЕСТ РЕДИРЕКТА ПО ЛОГОТИПУ ЯНДЕКСА ===")
        
        # Сохраняем текущее окно
        main_window = driver.current_window_handle
        print("✓ Сохранили основное окно")
        
        # Кликаем на логотип Яндекса
        main_page.click_yandex_logo()
        
        # Ждем открытия новой вкладки и переключаемся на нее
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        print("✓ Новая вкладка открыта")
        
        for window_handle in driver.window_handles:
            if window_handle != main_window:
                driver.switch_to.window(window_handle)
                break
        
        # Ждем загрузки страницы Дзена
        WebDriverWait(driver, 15).until(
            lambda d: "dzen.ru" in d.current_url or "yandex" in d.current_url
        )
        
        current_url = driver.current_url
        print(f"✓ Текущий URL: {current_url}")
        
        assert "dzen.ru" in current_url or "yandex" in current_url
        print("✓ Успешно перешли на страницу Дзена")
        
        # Закрываем вкладку и возвращаемся обратно
        driver.close()
        driver.switch_to.window(main_window)
        print("✓ Вернулись в основное окно")