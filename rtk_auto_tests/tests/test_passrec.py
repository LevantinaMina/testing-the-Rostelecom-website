import time


def test_tc_passrec_001_go_to_password_recovery(open_password_recovery_page):
    """TC-PASSREC-001: Переход на восстановление пароля"""
    recovery_page = open_password_recovery_page

    # Проверяем, что открылась форма восстановления
    assert "Восстановление пароля" in recovery_page.get_page_title_text()

    # Проверяем наличие всех элементов
    assert recovery_page.page_title.is_presented()
    assert recovery_page.page_description.is_presented()
    assert recovery_page.phone_tab.is_presented()
    assert recovery_page.email_tab.is_presented()
    assert recovery_page.login_tab.is_presented()
    assert recovery_page.ls_tab.is_presented()

    # По умолчанию активен таб "Телефон"
    assert recovery_page.get_active_tab_name() == "phone"


def test_recovery_with_invalid_phone(open_password_recovery_page):
    """Дополнительный тест: Восстановление с несуществующим номером"""
    recovery_page = open_password_recovery_page

    # Пытаемся восстановить с несуществующим номером
    recovery_page.username_field.send_keys("+79999999999")
    recovery_page.continue_button.click()
    time.sleep(2)

    # Проверяем сообщение об ошибке
    error_text = recovery_page.get_error_text()
    assert "Неверный логин или текст с картинки" in error_text or error_text != ""


def test_recovery_empty_field(open_password_recovery_page):
    """Дополнительный тест: Восстановление с пустым полем"""
    recovery_page = open_password_recovery_page

    # Оставляем поле пустым и нажимаем "Продолжить"
    recovery_page.continue_button.click()
    time.sleep(2)

    # Проверяем ошибку
    error_text = recovery_page.is_field_error_displayed()
    assert error_text != ""


def test_recovery_auto_switch_tabs(open_password_recovery_page):
    """Дополнительный тест: Автопереключение табов при вводе"""
    recovery_page = open_password_recovery_page

    # Переключаемся на таб "Почта"
    recovery_page.select_recovery_method('email')
    assert recovery_page.get_active_tab_name() == "email"

    # Вводим номер телефона
    recovery_page.username_field.send_keys("+79245336296")

    # КЛИКАЕМ НА ПОЛЕ КАПЧИ для активации валидации
    recovery_page.captcha_field.click()
    time.sleep(1)

    # Таб должен автоматически переключиться на "Номер"
    assert recovery_page.get_active_tab_name() == "phone"


#python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_passrec.py
