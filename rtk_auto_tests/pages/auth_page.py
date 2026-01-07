import time
from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


class AuthPage(WebPage):
    def __init__(self, web_driver, url=''):
        url = 'https://b2c.passport.rt.ru/'
        super().__init__(web_driver, url)

    # Элементы страницы авторизации
    username_field = WebElement(id='username')
    password_field = WebElement(id='password')

    # Табы выбора типа авторизации
    phone_tab = WebElement(id='t-btn-tab-phone')
    email_tab = WebElement(id='t-btn-tab-mail')
    login_tab = WebElement(id='t-btn-tab-login')
    ls_tab = WebElement(id='t-btn-tab-ls')

    # Кнопки
    submit_button = WebElement(id='kc-login')
    forgot_password_link = WebElement(xpath='//a[@id="forgot_password"]')
    register_link = WebElement(xpath='//a[@id="kc-register"]')

    # Активный таб
    active_tab = WebElement(css_selector='.rt-tab.rt-tab--small.rt-tab--active')

    # Заголовок страницы
    page_title = WebElement(css_selector='h1.card-container_title')

    # Элементы для ошибок
    error_message = WebElement(id='form-error-message')
    field_errors = ManyWebElements(css_selector='.rt-input-container__meta--error')

    def get_active_tab_name(self):
        """Получение названия активного таба"""
        if self.active_tab.is_presented():
            active = self.active_tab.get_text()
            if "Номер" in active or "Телефон" in active:
                return "phone"
            elif "Почта" in active:
                return "email"
            elif "Логин" in active:
                return "login"
            elif "Лицевой счёт" in active:
                return "ls"
        return ""

    def login(self, username, password):
        """Выполнение авторизации"""
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.submit_button.click()
        time.sleep(2)

    def select_auth_method(self, method):
        """Выбор метода авторизации"""
        methods = {
            'phone': self.phone_tab,
            'email': self.email_tab,
            'login': self.login_tab,
            'ls': self.ls_tab
        }
        if method in methods:
            methods[method].click()
            time.sleep(0.5)

    def get_error_text(self):
        """Получение текста ошибки авторизации"""
        if self.error_message.is_presented():
            return self.error_message.get_text()
        return ""

    def get_all_errors(self):
        """Получение всех ошибок на странице"""
        errors = []
        time.sleep(0.5)

        if self.field_errors.is_presented():
            error_elements = self.field_errors.find()
            for element in error_elements:
                if element.is_displayed():
                    text = element.text.strip()
                    if text:
                        errors.append(text)

        return errors

    def is_logged_in(self):
        """Проверка: нет полей логина И пароля"""
        time.sleep(2)
        return not (self.username_field.is_presented() and self.password_field.is_presented())