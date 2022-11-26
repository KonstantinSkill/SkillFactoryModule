import os.path
from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password, alien_email, alien_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result



def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/kung_fu_cat.jpeg'):
    """Проверяем что можно добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_update_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

### Задание 19.7.2
### Часть 2

# Тест 1
def test_post_add_new_pet_without_photo(name='Барбариска', animal_type='Котэ', age=3):
    """Проверяем возможность добавления питомца без фото"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фото
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


# Тест 2
def test_post_add_photo_of_pet(pet_photo='images/cat_intrig.jpeg'):
    """Проверяем возможность добавления фото к питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)


    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
    else:
        raise Exception("There is no my pets")


# Тест 3
def test_invalid_email(email=invalid_email, password=valid_password):
    """Проверяем, что запрос авторизации с отсутствующем в базе email"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Ожидаем статус не равный 200
    assert status != 200

# Тест 4
def test_invalid_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос авторизации с отсутствующем в базе паролем"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Ожидаем статус не равный 200
    assert status != 200

# Тест 5
def test_post_add_new_pet_simple_empty (name='', animal_type='', age=''):
    """Проверяем что можно просто создать карточку питомца с пустыми данными"""

    # Отправляем запрос на авторизацию
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создание питомца без фото
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result ['name'] == name


# Тест 6
def test_post_add_new_pet_not_valid (name='%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
                                     animal_type='%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%',
                                     age=-123456788901223456789012345678901234567890):
    """Проверяем что можно просто создать карточку питомца с не подходящим именем и породой"""

    # Отправляем запрос на авторизацию
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Создание питомца без фото
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result ['name'] == name


# Тест 7
def test_successful_update_pet_info_incorrect(name='Боб>', animal_type='Собакен', age='Десять'):
    """Проверяем возможность обновления информации о питомце на внесение возраста строкой"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и возраст питомца соответствует заданному
        assert status == 200
        assert result['age'] == age
    else:
        raise Exception("There is no my pets")

# Тест 8
def test_delete_alien_pet ():
    """Проверяем возможность удаления чужого питомца -
    если тест пройдёт удачно, значит любой авторизованный пользователь
    может удалить карточку любого чужого питомца, зная его ID"""

    # Авторизация стороннего пользователя
    _, alien_key = pf.get_api_key(alien_email, alien_password)

    # Отправляем запрос на свою авторизацию и получаем список своих питомцев и ID последнего добавленного
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    # Отправляем запрос на удаление используя данные стороннего пользователя
    status, _ = pf.delete_pet (alien_key, pet_id)

    # Проверяем что статус ответа равен 200 и в списке питомцев нет ID удалённого питомца
    if status == 200:
        print ('\nЛюбой авторизованный пользователь может '
               'удалить любого чужого питомца, зная его ID')

    assert status == 200
    assert pet_id not in my_pets.values ()

# Тест 9
def test_post_add_photo_of_alien_pet(pet_photo='images/kung_fu_cat.jpeg'):
    """Проверяем возможность добавления фото к чужому питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Авторизация злоумышленника и печать его KEY
    _, alien_key = pf.get_api_key(alien_email, alien_password)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.post_add_photo_of_pet(alien_key, my_pets['pets'][0]['id'], pet_photo)

    if status == 200:
        print('\nЛюбой авторизованный пользователь может'
              'добавить или поменять фото любого чужого питомца, зная его ID')

        # Сверяем полученный ответ с ожидаемым результатом
    assert status != 200

# Тест 10

def test_successful_update_alien_pet_info(name='Робоцып', animal_type='Мышь', age=100):
    """Проверяем возможность обновления информации чужого питомца"""

    # Авторизация злоумышленника и печать его KEY
    _, alien_key = pf.get_api_key(alien_email, alien_password)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    status, result = pf.update_pet_info(alien_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if status == 200:
        print ('\nЛюбой авторизованный пользователь может '
               'изменить данные любого чужого питомца, зная его ID')

    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result ['name'] == name
