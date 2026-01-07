import time


def test_tc_auth_001_success_auth_by_phone(auth_page):
    """TC-AUTH-001: Успешная авторизация по номеру телефона"""
    page = auth_page

    # Проверяем, что активен таб "Номер" (по умолчанию)
    assert page.get_active_tab_name() == "phone"

    # Вводим данные
    page.login(
        username="+79245336296",
        password="Qwepoi123"
    )

    # Проверяем успешную авторизацию
    time.sleep(3)
    assert page.is_logged_in()


def test_tc_auth_002_error_auth_wrong_password(auth_page):
    """TC-AUTH-002: Ошибка авторизации с неверным паролем"""
    page = auth_page

    # Убеждаемся, что активен таб "Номер"
    page.select_auth_method('phone')

    # Вводим валидный номер и неверный пароль
    page.login(
        username="+79245336296",
        password="invalidPass123!"
    )

    # Проверяем сообщение об ошибке
    error_text = page.get_error_text()
    assert "Неверный логин или пароль" in error_text


def test_tc_auth_003_auth_with_empty_phone(auth_page):
    """TC-AUTH-003: Авторизация с пустым номером телефона"""
    page = auth_page

    # Убеждаемся, что активен таб "Номер"
    page.select_auth_method('phone')

    # Оставляем поле номера пустым, вводим пароль
    page.password_field.send_keys("Qwepoi123")
    page.submit_button.click()
    time.sleep(1)

    # Проверяем сообщение об ошибке
    errors = page.get_all_errors()
    assert len(errors) > 0


def test_tc_auth_004_auth_with_invalid_phone_format(auth_page):
    """TC-AUTH-004: Авторизация с некорректным форматом номера"""
    page = auth_page

    page.select_auth_method('phone')

    # Вводим короткий номер
    page.username_field.send_keys("123")
    page.password_field.send_keys("any_password")
    page.submit_button.click()
    time.sleep(1)

    # Проверяем ошибку
    errors = page.get_all_errors()
    assert len(errors) > 0


def test_tc_auth_005_auto_switch_tab_when_entering_phone(auth_page):
    """TC-AUTH-005: Автопереключение таба при вводе номера"""
    page = auth_page

    # Переключаемся на таб "Почта"
    page.select_auth_method('email')
    assert page.get_active_tab_name() == "email"

    # Вводим номер телефона
    page.username_field.send_keys("+79245336296")

    # Кликаем на поле пароля для активации валидации
    page.password_field.click()
    time.sleep(0.5)

    # Проверяем, что таб автоматически переключился на "Номер"
    assert page.get_active_tab_name() == "phone"


def test_tc_auth_006_success_auth_by_email(auth_page):
    """TC-AUTH-006: Успешная авторизация по почте"""
    page = auth_page

    # Переключаемся на таб "Почта"
    page.select_auth_method('email')

    # Вводим данные
    page.login(
        username="valya15fenichco.com@mail.ru",
        password="Qwepoi123"
    )

    # Проверяем успешную авторизацию
    time.sleep(3)
    assert page.is_logged_in()


def test_tc_auth_007_auth_with_nonexistent_email(auth_page):
    """TC-AUTH-007: Авторизация с несуществующим email"""
    page = auth_page

    # Переключаемся на таб "Почта"
    page.select_auth_method('email')

    # Вводим несуществующий email
    page.login(
        username="test@example.com",
        password="Qwepoi123"
    )

    # Проверяем ошибку
    error_text = page.get_error_text()
    assert "Неверный логин или пароль" in error_text


def test_tc_auth_008_success_auth_by_login(auth_page):
    """TC-AUTH-008: Успешная авторизация по логину"""
    page = auth_page

    # Переключаемся на таб "Логин"
    page.select_auth_method('login')

    # Вводим данные
    page.login(
        username="rtkid_1767435473996",
        password="Qwepoi123"
    )

    # Проверяем успешную авторизацию
    time.sleep(3)
    assert page.is_logged_in()


def test_tc_auth_009_auth_login_case_sensitive(auth_page):
    """TC-AUTH-009: Авторизация по логину в разных регистрах"""
    page = auth_page

    page.select_auth_method('login')

    # Вводим логин заглавными буквами
    page.login(
        username="RTKID_1767435473996",  # заглавными буквами
        password="Qwepoi123"
    )

    # Проверяем результат
    time.sleep(3)

    error_text = page.get_error_text()
    assert "Неверный логин или пароль" in error_text


def test_tc_auth_010_success_auth_by_ls(auth_page):
    """TC-AUTH-010: Успешная авторизация по лицевому счету"""
    page = auth_page

    # Переключаемся на таб "Лицевой счет"
    page.select_auth_method('ls')

    # Вводим данные
    page.login(
        username="123456789012",  # ← замени на действительный лицевой счет
        password="Qwepoi123"  # ← замени на соответсвующий пароль
    )

    # Проверяем успешную авторизацию
    time.sleep(3)
    assert page.is_logged_in()


def test_tc_auth_011_error_auth_nonexistent_ls(auth_page):
    """TC-AUTH-011: Ошибка при авторизации по несуществующему ЛС"""
    page = auth_page

    # Переключаемся на таб "Лицевой счет"
    page.select_auth_method('ls')

    # Вводим несуществующий лицевой счет
    page.login(
        username="99999999999",   # ← длина меньше 12 символов (11)
        password="Qwepoi123"
    )

    # Проверяем ошибку
    error_text = page.get_error_text()
    assert "" in ''


#python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_auth.py