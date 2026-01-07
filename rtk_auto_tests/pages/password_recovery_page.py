import time
from pages.base import WebPage
from pages.elements import WebElement
from pages.elements import ManyWebElements


class PasswordRecoveryPage(WebPage):
    def __init__(self, web_driver, url=''):
        url = 'https://b2c.passport.rt.ru/auth/realms/b2c/login-actions/reset-credentials'
        super().__init__(web_driver, url)

    # Основные элементы формы восстановления
    page_title = WebElement(id='card-title')
    page_description = WebElement(id='card-description')

    # Табы выбора типа восстановления
    phone_tab = WebElement(id='t-btn-tab-phone')
    email_tab = WebElement(id='t-btn-tab-mail')
    login_tab = WebElement(id='t-btn-tab-login')
    ls_tab = WebElement(id='t-btn-tab-ls')

    # Поле ввода
    username_field = WebElement(id='username')

    # Кнопка "Продолжить"
    continue_button = WebElement(id='reset')

    # Поле капчи
    captcha_field = WebElement(id='captcha')

    # Сообщения об ошибках
    error_message = WebElement(id='form-error-message')
    field_error_message = WebElement(css_selector='span.rt-input-container_meta.rt-input-container_meta--error')

    def select_recovery_method(self, method):
        """Выбор метода восстановления"""
        methods = {
            'phone': self.phone_tab,
            'email': self.email_tab,
            'login': self.login_tab,
            'ls': self.ls_tab
        }
        if method in methods:
            methods[method].click()
            time.sleep(0.5)

    def get_active_tab_name(self):
        """Получение названия активного таба"""
        try:
            tabs = [
                (self.phone_tab, 'phone'),
                (self.email_tab, 'email'),
                (self.login_tab, 'login'),
                (self.ls_tab, 'ls')
            ]

            for tab_element, tab_name in tabs:
                if tab_element.is_presented():
                    classes = tab_element.get_attribute('class') or ''
                    if 'rt-tab--active' in classes:
                        return tab_name
        except:
            pass
        return ""

    def get_error_text(self):
        """Получение текста общей ошибки формы"""
        if self.error_message.is_presented():
            return self.error_message.get_text()
        return ""


    def is_field_error_displayed(self):
        """Проверяет, отображается ли ошибка при пустом поле"""
        return self.field_error_message.is_presented()

    def get_page_title_text(self):
        """Получение текста заголовка страницы"""
        if self.page_title.is_presented():
            return self.page_title.get_text()
        return ""