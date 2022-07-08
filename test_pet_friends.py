from api import PetFriends
from settings import valid_email, valid_password , nonvalide_password , nonvalide_email
import os
import json

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    '''Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key'''

    status, result = pf.get_api_key(email, password)

    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filyer=''):
    ''' Проверяем что запрос всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
        запрашиваем список всех питомцев и проверяем что список не пустой.
        Доступное значение параметра filter - 'my_pets' либо'''

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filyer)

    assert status == 200
    assert  len(result['pets']) > 0

def test_add_new_pets_with_valid_key(name='рыжая', animal_type='лиса', age='3', pet_photo='images/fenek.jpg'):
    '''проверяем можно ли добавить питомца с корректными данными'''

    #получаем путь изображение питомца и сохраняем его в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status,result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Лиса", "белая", "2", "images/fenek.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_self_pet_info(name='Лисичка',animal_type='лиса',age='5'):
    '''проверяем обновление информации о питомце'''

# Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

# Если список пуст попробуем обновить его имя ,тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type,age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception('нет питомцев')

# Дополнительно 10 тестов по практике 19.2.7

def test_add_new_pet_without_photo (name = "лиса",animal_type="Лисичка",age='8'):
    '''проверяем создание нового питомца без фото'''

    # запрашиваем ключ api
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    #добовляем питомца
    status, result = pf.post_add_new_pet_without_photo(auth_key, name, animal_type, age,)

    #проверяем статус
    assert status == 200
    assert result['name'] == name,result['anumal_type'] == animal_type and result['age'] == age

def test_test_get_api_key_for_nonvalid_user(email=nonvalide_email, passwoord=nonvalide_password):
    """ Проверяем что запрос api ключа с недействительными email и паролем возвращает статус 403"""

    _, status = pf.get_api_key(email,passwoord)

    assert status != 403

def test_get_all_pets_with_invalid_filter(filter='pet'):
    """ Проверяем что запрос питомцев с недействительным значением фильтра возвращает статус 500"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, _ = pf.get_list_of_pets(auth_key, filter)

    assert status == 500

def test_post_change_pet_foto(pet_photo='images/fenek2.jpg'):
    """Проверяем добавление нового фото"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового (БЕЗ ФОТО) и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key,"лиса","лисичка","5",pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка
    pet_id = my_pets['pets'][0]['id']

    # Добавляем фото
    status, result = pf.post_change_pet_photo(auth_key, pet_id, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['pet_photo'] !=0

def test_add_new_pet_with_not_valid_data_faild(name='Лиса', animal_type='Лисичка',
                                               age='А', pet_photo='images/fenek.jpg'):
    """ Проверяем что можно добавить питомца с некорректными данными в раздел age """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age

def test_add_new_pet_with_nonvalide_faild(name='', animal_type='',
                                     age='', pet_photo='images/fenek.jpg'):
    """ Проверяем создание питомца с пустыми значениями в разделах name, animal_type,age """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['age'] == age ,result['name'] == name and result['animal_type'] == animal_type


def test_get_api_key_for_nonvalide_password(email=valid_email, password="12345"):
    """проверяем не верный пароль """
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями = 403
    assert status == 403
    assert 'key' is not result


def test_get_api_key_for_nonvalide_email(email='i.fkfkfkf@yandex.ru', password=valid_password):
    """проверяем не верный email """
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями = 403
    assert status == 403
    assert 'key' is not result

def test_delete_self_pet_without_id():
    """проверяем удаление питомца без указание id"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "King-Kong", "Gorila", "133", r'../images/king-kong2.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = ""
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 404 и в списке питомцев нет id удалённого питомца

    assert status == 404
    assert pet_id not in my_pets.values()

def test_successful_update_self_pet_info_numbers(name='55555', animal_type='66666', age=6):
    """Проверяем возможность обновления значений name, animal_type о питомце только цифрами"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")
