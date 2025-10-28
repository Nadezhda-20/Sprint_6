import pytest
import time
from pages.main_page import MainPage


class TestQuestions:
    @pytest.mark.parametrize("question_index,expected_text", [
        (0, "Сутки — 400 рублей. Оплата курьеру — наличными или картой."),
        (1, "Пока что у нас так: один заказ — один самокат. Если хотите покататься с друзьями, можете просто сделать несколько заказов — один за другим."),
        (2, "Допустим, вы оформляете заказ на 8 мая. Мы привозим самокат 8 мая в течение дня. Отсчёт времени аренды начинается с момента, когда вы оплатите заказ курьеру. Если мы привезли самокат 8 мая в 20:30, суточная аренда закончится 9 мая в 20:30."),
        (3, "Только начиная с завтрашнего дня. Но скоро станем расторопнее."),
        (4, "Пока что нет! Но если что-то срочное — всегда можно позвонить в поддержку по красивому номеру 1010."),
        (5, "Самокат приезжает к вам с полной зарядкой. Этого хватает на восемь суток — даже если будете кататься без передышек и во сне. Зарядка не понадобится."),
        (6, "Да, пока самокат не привезли. Штрафа не будет, объяснительной записки тоже не попросим. Все же свои."),
        (7, "Да, обязательно. Всем самокатов! И Москве, и Московской области.")
    ])
    def test_question_dropdown(self, driver, question_index, expected_text):
        main_page = MainPage(driver)
        
        # Прокручиваем к вопросам
        first_question = main_page.find_element(main_page.QUESTION_LOCATORS[0])
        driver.execute_script("arguments[0].scrollIntoView();", first_question)
        time.sleep(1)
        
        # Кликаем на вопрос
        main_page.click_question(question_index)
        
        # Даем время для анимации
        time.sleep(2)
        
        # Получаем текст ответа
        answer_text = main_page.get_answer_text(question_index)
        
        assert answer_text == expected_text, f"Текст ответа не совпадает для вопроса {question_index}"