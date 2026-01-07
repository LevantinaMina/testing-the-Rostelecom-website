# pages/registration_page.py
import time
from pages.elements import WebElement
from pages.elements import ManyWebElements


class RegistrationPage:
    """Страница регистрации"""

    def __init__(self, driver):
        self.driver = driver
        # Инициализируем элементы с правильными локаторами
        self._init_elements()

    def _init_elements(self):
        """Инициализация элементов с правильными локаторами"""
        # Заголовок
        self.page_title = WebElement(xpath='//h1[@id="card-title" and @class="card-container__title"]')

        # Поля формы
        self.first_name_field = WebElement(name='firstName')
        self.last_name_field = WebElement(name='lastName')

        # Регион (это 3й input по списку)
        self.region_field = WebElement(xpath='(//input[@type="text"])[3]')
        self.region_options = ManyWebElements(xpath='//div[contains(@class, "rt-select__list-item")]')

        # Email/телефон
        self.email_phone_field = WebElement(id='address')

        # Пароли
        self.password_field = WebElement(id='password')
        self.confirm_password_field = WebElement(id='password-confirm')

        # Кнопка регистрации - ВЕРНЫЙ локатор!
        self.register_button = WebElement(xpath='//button[@name="register"]')

        # Ошибки
        self.all_error_messages = ManyWebElements(xpath='//span[contains(@class, "rt-input-container__meta--error")]')
        self.password_error = WebElement(xpath='//*[@id="password"]/../following-sibling::span')

    def _setup_element(self, element):
        """Настройка элемента для работы"""
        if element:
            element._web_driver = self.driver
        return element

    def select_region(self, region_name):
        """Выбор региона из выпадающего списка"""
        try:
            field = self._setup_element(self.region_field)
            field.click()
            time.sleep(0.5)
            field.send_keys(region_name)
            time.sleep(1)

            # Кликаем на первый вариант
            options = self._setup_element(self.region_options)
            if options.count() > 0:
                options[0].click()
        except Exception as e:
            print(f"Ошибка при выборе региона: {e}")

    def get_password_error_text(self):
        """Получение текста ошибки для поля пароля"""
        time.sleep(0.5)
        error = self._setup_element(self.password_error)

        if error.is_presented():
            return error.get_text()

        errors = self.get_all_errors()
        for err in errors:
            if 'парол' in err.lower():
                return err

        return ""

    def get_all_errors(self):
        """Получение всех сообщений об ошибках на странице"""
        errors = []
        time.sleep(0.5)

        error_elements = self._setup_element(self.all_error_messages)
        if error_elements.is_presented():
            elements = error_elements.find()
            for element in elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        errors.append(text)

        return errors

    def get_title_text(self):
        """Получение текста заголовка"""
        return self._setup_element(self.page_title).get_text()