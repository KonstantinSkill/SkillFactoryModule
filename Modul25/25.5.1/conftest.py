import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome(
        '/media/jinnd/Jinn/Obuchenie/Skillfactory/Python/modul25/chromedriver_directory/chromedriver')

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    yield

    pytest.driver.quit()

@pytest.fixture()
### открывается авторизованная страница с питомцами
def show_my_pets():
    # Вводим email и пароль
    pytest.driver.find_element(By.ID, 'email').send_keys("123qweasd@ewq.ru")
    pytest.driver.find_element(By.ID, 'pass').send_keys("1234")

    # Развертывание страницы во весь экран
    pytest.driver.maximize_window()

    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Нажимаем на пункт меню "Мои питомцы"
    pytest.driver.find_element(By.XPATH, '//*[@href=\"/my_pets\"]').click()

