import pytest
import time
from pages.auth_page import AuthPage
from pages.registration_page import RegistrationPage
from pages.password_recovery_page import PasswordRecoveryPage


@pytest.fixture
def auth_page(selenium):
    """Фикстура для страницы авторизации"""
    page = AuthPage(selenium)
    time.sleep(2)
    return page


@pytest.fixture
def open_registration_page(selenium):
    """Фикстура для открытия страницы регистрации"""
    from pages.auth_page import AuthPage
    auth_page = AuthPage(selenium)
    time.sleep(2)
    auth_page.register_link.click()
    time.sleep(3)
    return RegistrationPage(selenium)


@pytest.fixture
def open_password_recovery_page(selenium):
    """Фикстура для открытия страницы восстановления пароля"""
    auth_page = AuthPage(selenium)
    time.sleep(2)
    auth_page.forgot_password_link.click()
    time.sleep(3)
    return PasswordRecoveryPage(selenium)
