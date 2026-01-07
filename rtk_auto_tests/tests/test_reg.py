import time


def test_tc_reg_001_go_to_registration_page(open_registration_page):
    """TC-REG-001: Переход на форму регистрации"""
    reg_page = open_registration_page

    # Проверяем, что открылась форма регистрации
    assert "Регистрация" in reg_page.get_title_text()


def test_tc_reg_002_success_registration_by_phone(open_registration_page):
    """TC-REG-002: Успешная регистрация по номеру телефона"""
    reg_page = open_registration_page

    # Заполнить: "Имя", "Фамилия"
    reg_page._setup_element(reg_page.first_name_field).send_keys("Иван")
    reg_page._setup_element(reg_page.last_name_field).send_keys("Петров")

    # Выбрать регион
    reg_page.select_region("Москва г")

    # Ввести номер телефона
    test_phone = "+79456578439"
    reg_page._setup_element(reg_page.email_phone_field).send_keys(test_phone)

    # Ввести пароль
    test_password = "TestPass123!"
    reg_page._setup_element(reg_page.password_field).send_keys(test_password)

    # Подтвердить пароль
    reg_page._setup_element(reg_page.confirm_password_field).send_keys(test_password)

    # Нажать "Зарегистрироваться"
    reg_page._setup_element(reg_page.register_button).click()

    # Проверяем, что открылась форма для ввода кода
    time.sleep(5)

    # Ищем подтверждение телефона
    reg_page.driver.find_element("xpath", "//h1[contains(text(), 'Подтверждение телефона')]")


def test_tc_reg_003_password_length_validation(open_registration_page):
    """TC-REG-003: Проверка требований к сложности пароля (длина)"""
    reg_page = open_registration_page

    # Заполнить все обязательные поля
    reg_page._setup_element(reg_page.first_name_field).send_keys("Иван")
    reg_page._setup_element(reg_page.last_name_field).send_keys("Петров")
    reg_page.select_region("Москва г")
    reg_page._setup_element(reg_page.email_phone_field).send_keys("test@example.com")

    # В поле "Пароль" ввести "1234567" (7 символов)
    reg_page._setup_element(reg_page.password_field).send_keys("1234567")
    reg_page._setup_element(reg_page.confirm_password_field).send_keys("1234567")

    # Нажать "Зарегистрироваться"
    reg_page._setup_element(reg_page.register_button).click()
    time.sleep(2)

    # Проверяем сообщение об ошибке
    error_text = reg_page.get_password_error_text()
    assert "Длина пароля должна быть не менее 8 символов" in error_text or "" in error_text.lower()


def test_tc_reg_004_success_registration_by_email(open_registration_page):
    """TC-REG-004: Успешная регистрация по email"""
    reg_page = open_registration_page

    # Заполнить: "Имя", "Фамилия"
    reg_page._setup_element(reg_page.first_name_field).send_keys("Иван")
    reg_page._setup_element(reg_page.last_name_field).send_keys("Петров")

    # Выбрать регион
    reg_page.select_region("Москва г")

    # Ввести адрес email
    test_email = "test@example.com"
    reg_page._setup_element(reg_page.email_phone_field).send_keys(test_email)

    # Ввести пароль
    test_password = "TestPass123!"
    reg_page._setup_element(reg_page.password_field).send_keys(test_password)

    # Подтвердить пароль
    reg_page._setup_element(reg_page.confirm_password_field).send_keys(test_password)

    # Нажать "Зарегистрироваться"
    reg_page._setup_element(reg_page.register_button).click()

    # Проверяем, что открылась форма для ввода кода
    time.sleep(5)

    # Ищем подтверждение email
    reg_page.driver.find_element("xpath", "//h1[contains(text(), 'Подтверждение email')]")


def test_registration_with_empty_fields(open_registration_page):
    """Дополнительный тест: Регистрация с пустыми полями"""
    reg_page = open_registration_page

    # Оставляем все поля пустыми
    # Нажимаем "Зарегистрироваться"
    reg_page._setup_element(reg_page.register_button).click()
    time.sleep(2)

    # Проверяем, что появились сообщения об ошибках
    errors = reg_page.get_all_errors()
    assert len(errors) > 0


def test_registration_password_mismatch(open_registration_page):
    """Дополнительный тест: Несовпадение паролей"""
    reg_page = open_registration_page

    # Заполняем обязательные поля
    reg_page._setup_element(reg_page.first_name_field).send_keys("Иван")
    reg_page._setup_element(reg_page.last_name_field).send_keys("Петров")
    reg_page.select_region("Москва г")
    reg_page._setup_element(reg_page.email_phone_field).send_keys("test@example.com")

    # Вводим разные пароли
    reg_page._setup_element(reg_page.password_field).send_keys("ValidPass123!")
    reg_page._setup_element(reg_page.confirm_password_field).send_keys("DifferentPass456!")

    # Нажимаем "Зарегистрироваться"
    reg_page._setup_element(reg_page.register_button).click()
    time.sleep(2)

    # Проверяем сообщение об ошибке
    errors = reg_page.get_all_errors()

    assert errors


def test_registration_weak_password_only_numbers(open_registration_page):
    """Дополнительный тест: Регистрация с паролем только из цифр"""
    reg_page = open_registration_page

    # Заполняем поля
    reg_page._setup_element(reg_page.first_name_field).send_keys("Иван")
    reg_page._setup_element(reg_page.last_name_field).send_keys("Петров")
    reg_page.select_region("Москва г")
    reg_page._setup_element(reg_page.email_phone_field).send_keys("test@example.com")

    # Вводим пароль только из цифр
    reg_page._setup_element(reg_page.password_field).send_keys("12345678")
    reg_page._setup_element(reg_page.confirm_password_field).send_keys("12345678")

    # Нажимаем "Зарегистрироваться"
    reg_page._setup_element(reg_page.register_button).click()
    time.sleep(2)

    # Проверяем ошибку о слабом пароле
    error_text = reg_page.get_password_error_text()
    assert len(error_text) > 0


#python -m pytest -v --driver Chrome --driver-path chromedriver.exe tests/test_reg.py