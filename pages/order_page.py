from .base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


class OrderPage(BasePage):
    # Локаторы для первой страницы заказа
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Имя']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='* Фамилия']")
    ADDRESS_INPUT = (By.XPATH, "//input[@placeholder='* Адрес: куда привезти заказ']")
    METRO_STATION_INPUT = (By.XPATH, "//input[@placeholder='* Станция метро']")
    METRO_STATION_OPTION = (By.XPATH, "//li[@class='select-search__row']//button")  # Первая станция в списке
    PHONE_INPUT = (By.XPATH, "//input[@placeholder='* Телефон: на него позвонит курьер']")
    NEXT_BUTTON = (By.XPATH, "//button[text()='Далее']")

    # Локаторы для второй страницы заказа
    DELIVERY_DATE_INPUT = (By.XPATH, "//input[@placeholder='* Когда привезти самокат']")
    RENTAL_PERIOD_DROPDOWN = (By.XPATH, "//div[contains(@class, 'Dropdown-control')]")
    RENTAL_PERIOD_OPTION = (By.XPATH, "//div[contains(@class, 'Dropdown-option') and text()='сутки']")
    RENTAL_PERIOD_OPTION_TWO_DAYS = (By.XPATH, "//div[contains(@class, 'Dropdown-option') and text()='двое суток']")
    COLOR_BLACK_CHECKBOX = (By.ID, "black")
    COLOR_GREY_CHECKBOX = (By.ID, "grey")
    COMMENT_INPUT = (By.XPATH, "//input[@placeholder='Комментарий для курьера']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Заказать' and contains(@class, 'Button_Middle')]")

    # Локаторы для модального окна подтверждения
    MODAL_CONFIRM = (By.XPATH, "//div[contains(@class, 'Order_Modal')]")
    CONFIRM_ORDER_BUTTON = (By.XPATH, "//button[text()='Да']")
    SUCCESS_MESSAGE = (By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]")

    def fill_first_page(self, first_name, last_name, address, phone):
        print("Заполняем первую страницу заказа...")
        
        # Заполняем основные поля
        self.input_text(self.FIRST_NAME_INPUT, first_name)
        self.input_text(self.LAST_NAME_INPUT, last_name)
        self.input_text(self.ADDRESS_INPUT, address)
        
        # Выбор станции метро - более надежный способ
        print("Выбираем станцию метро...")
        metro_input = self.find_element(self.METRO_STATION_INPUT)
        metro_input.click()
        
        # Ждем появления списка станций
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "select-search__options"))
        )
        
        # Выбираем первую доступную станцию
        first_station = self.driver.find_element(By.XPATH, "//li[@class='select-search__row']//button")
        first_station.click()
        print("Станция метро выбрана")
        
        # Заполняем телефон
        self.input_text(self.PHONE_INPUT, phone)
        
        # Скриншот перед переходом
        self.take_screenshot("first_page_filled")
        
        # Переходим на следующую страницу
        self.click_element(self.NEXT_BUTTON)
        print("Переход на вторую страницу...")

    def fill_second_page(self, delivery_date, rental_period, color, comment):
        print("Заполняем вторую страницу заказа...")
        
        # Ждем загрузки второй страницы
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.DELIVERY_DATE_INPUT)
        )
        
        # Заполнение даты - используем более надежный метод
        print(f"Вводим дату доставки: {delivery_date}")
        date_input = self.find_element(self.DELIVERY_DATE_INPUT)
        
        # Очищаем поле и вводим дату
        date_input.click()
        date_input.clear()
        
        # Вводим дату по частям для надежности
        for char in delivery_date:
            date_input.send_keys(char)
            time.sleep(0.1)
        
        # Нажимаем Enter для применения
        date_input.send_keys(Keys.ENTER)
        time.sleep(1)
        
        # Выбор срока аренды
        print(f"Выбираем срок аренды: {rental_period}")
        dropdown = self.find_element(self.RENTAL_PERIOD_DROPDOWN)
        dropdown.click()
        time.sleep(1)
        
        if rental_period == "сутки":
            option = self.find_clickable_element(self.RENTAL_PERIOD_OPTION)
            option.click()
        elif rental_period == "двое суток":
            option = self.find_clickable_element(self.RENTAL_PERIOD_OPTION_TWO_DAYS)
            option.click()
        print("Срок аренды выбран")
        
        # Выбор цвета
        print(f"Выбираем цвет: {color}")
        if color == "black":
            checkbox = self.find_element(self.COLOR_BLACK_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
        elif color == "grey":
            checkbox = self.find_element(self.COLOR_GREY_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
        print("Цвет выбран")
        
        # Комментарий (необязательное поле)
        if comment:
            self.input_text(self.COMMENT_INPUT, comment)
            print(f"Введен комментарий: {comment}")
        
        # Скриншот перед заказом
        self.take_screenshot("second_page_filled")
        
        # Нажатие кнопки Заказать
        print("Нажимаем кнопку 'Заказать'...")
        order_button = self.find_clickable_element(self.ORDER_BUTTON)
        
        # Прокручиваем к кнопке и кликаем
        self.driver.execute_script("arguments[0].scrollIntoView();", order_button)
        time.sleep(1)
        order_button.click()
        print("Кнопка 'Заказать' нажата")

    def wait_for_confirm_modal(self):
        """Ожидание появления модального окна подтверждения"""
        print("Ожидаем появление модального окна подтверждения...")
        
        # Пробуем разные локаторы для модального окна
        modal_selectors = [
            "//div[contains(@class, 'Order_Modal')]",
            "//div[contains(@class, 'Modal_modal')]",
            "//div[@class='Order_Modal__YZ-d3']"
        ]
        
        for selector in modal_selectors:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, selector))
                )
                print(f"Модальное окно найдено по селектору: {selector}")
                self.take_screenshot("confirm_modal_appeared")
                return True
            except:
                continue
        
        # Если модальное окно не найдено, проверяем наличие ошибок
        self.check_for_errors()
        return False

    def check_for_errors(self):
        """Проверка наличия сообщений об ошибках"""
        error_selectors = [
            "//div[contains(@class, 'Input_ErrorMessage')]",
            "//div[contains(@class, 'error')]",
            "//span[contains(@class, 'error')]"
        ]
        
        for selector in error_selectors:
            errors = self.driver.find_elements(By.XPATH, selector)
            if errors:
                error_texts = [error.text for error in errors if error.text]
                if error_texts:
                    print(f"Обнаружены ошибки: {error_texts}")
                    self.take_screenshot("errors_detected")
                    return True
        
        print("Ошибок не обнаружено")
        return False

    def confirm_order(self):
        print("Подтверждаем заказ...")
        if self.wait_for_confirm_modal():
            # Пробуем разные локаторы для кнопки подтверждения
            confirm_selectors = [
                "//button[text()='Да']",
                "//button[contains(@class, 'Button_Middle') and text()='Да']"
            ]
            
            for selector in confirm_selectors:
                try:
                    confirm_button = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    confirm_button.click()
                    print("Заказ подтвержден")
                    return
                except:
                    continue
            
            raise Exception("Не удалось найти кнопку подтверждения заказа")
        else:
            raise Exception("Модальное окно подтверждения не появилось")

    def get_success_message(self):
        print("Ожидаем сообщение об успешном заказе...")
        
        # Ждем появления сообщения об успехе
        success_element = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'Order_ModalHeader')]"))
        )
        message = success_element.text
        print(f"Получено сообщение: {message}")
        self.take_screenshot("success_message")
        return message