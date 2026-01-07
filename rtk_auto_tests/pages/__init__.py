from .base import WebPage
from .elements import WebElement, ManyWebElements
from .auth_page import AuthPage
from .registration_page import RegistrationPage
from .password_recovery_page import PasswordRecoveryPage

__all__ = ['WebPage', 'WebElement', 'ManyWebElements', 'AuthPage', 'RegistrationPage', 'PasswordRecoveryPage']