import os
from api import PetFriends
from settings import *

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):  # получение key
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result  # наличие key в result
    print(f'***API ключ: {status},\n{result}')


def test_get_all_pets_with_valid_key(filter='my_pets'):  # список питомцев по фильтру
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
    print(f'***Список питомцев: {status},\n{result}')


def test_add_new_pet_with_valid_data(name='Люцифер', animal_type='cat', age='1', pet_photo='images/cat.jpg'): # добавления нового питомца с корректными данными
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) # запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) # добавление питомца
    assert status == 200
    assert result['name'] == name
    print(f'***Новый питомец: {status},\n{result}')


def test_successful_delete_self_pet():  # возможность удаления питомца
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # получение и сохранение ключа
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # запрос списка всех питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "NewPet", "newpet", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']  # Берём id первого питомца из списка и отправляем запрос на удаление
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")  # Ещё раз запрашиваем список своих питомцев
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()
    print("***Питомец с ID: ", pet_id, "удалён")


def test_successful_update_self_pet_info(name='Аид', animal_type='wolf', age=5): # тест возможность обновить информацию о питомце
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Получаем ключ в auth_key и список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:  # Если список не пустой, то пробуем обновить его имя, тип и возраст
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200   # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert result['name'] == name
        print(result, "Обновлено")
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")


def test_add_pet_with_valid_data_empty(name='', animal_type='', age='', pet_photo='images/cat.jpg'):  #добавление нового питомца с пустыми значениями
    _, api_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name
    print(f'***Добавлен питомец с пустыми значениями полей: "name", "animal_type", "age". ( {result})')


def test_add_new_pet_with_valid_data_without_photo(name = 'Люцифер', animal_type = 'cat', age = '1'):  # добавление нового питомца с корректными данными без изображения
    #pet_photo = os.path.join(os.path.dirname(__file__))  # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)  # добавление питомца
    assert status == 200
    assert result['name'] == name
    print(f'***Новый питомец (без фото): {status},\n{result}')


def test_successful_add_pet_photo(pet_photo='images/dog.jpg'):  # тест возможность добавить фото питомцу
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)  # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password)  # Получаем ключ в auth_key и список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:  # Если список не пустой, то пробуем обновить его фото
        status, result = pf.add_photo_of_a_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
        assert status == 200  # Проверяем что статус ответа = 200 и фото соответствует заданному
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
        print(result, "Добвалено фото")
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_with_Invalid_email(email=wrong_email, password=valid_password): #тест получение ключа при неверном email
    status, result = pf.get_api_key(email, password)
    #assert status == 200
    assert 'key' not in result  # наличие key в result
    print(f'***Неверный email, код: {status},\n{result}')


def test_get_api_key_with_Invalid_password(email=valid_email, password=wrong_password): # тест получение ключа при неверном пароле
    status, result = pf.get_api_key(email, password)
    assert 'key' not in result  # наличие key в result
    print(f'***Неверный пароль, код: {status},\n{result}')


def test_get_api_key_with_Invalid_password_Invalid_email(email=wrong_email, password=wrong_password): # тест получение ключа при неверных email и пароле
    status, result = pf.get_api_key(email, password)
    assert 'key' not in result  # наличие key в result
    print(f'***Неверный email и неверный пароль, код: {status},\n{result}')


def test_get_all_pets_with_valid_key_with_Invalid_Filter(filter='My_pets'):  # тест вывод списка питомцев по фильтру при неверном значении фильтра
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 500
    print(f'***Значение filter: {filter} недоступно, код: {status}')


def test_add_new_pet_with_Invalid_data_photo(name='Люцифер', animal_type='dog', age='5', pet_photo='images/dog.jpg'): #тест добавления нового питомца с неправильным путём к фото
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo

    if not os.path.exists(pet_photo):  # проверка наличия фото при добавлении питомца
        print(f'\n Фото не найдено! Использовано фото dog {pet_photo}')
        pet_photo = "images/dog.jpg" #использовать доступное фото

    _, auth_key = pf.get_api_key(valid_email, valid_password) #запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) #добавление питомца
    assert status == 200
    assert result['name'] == name
    print(f'***Новый питомец: {status},\n{result}')


def test_add_new_pet_with_Invalid_data_age(name='Люцифер', animal_type='cat', age='-1', pet_photo='images/cat.jpg'): # тест добавления нового питомца с отрицательным возрастом
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) # запрос api-ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) #добавление питомца
    assert status == 200
    assert (float(age) < 0)
    print(f'Статус код: {status}, при добавлении питомца с отрицательным возрастом! ({age})')
    print(f'***Новый питомец: {status},\n{result}')


def test_add_new_pet_with_Invalid_data_format(name='Люцифер', animal_type='cat', age="twentyone'", pet_photo='images/cat.jpg'): # тест добавления нового питомца с текстом в поле возраст
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo) # получение полного пути изображения и его сохранение в переменную pet_photo
    _, auth_key = pf.get_api_key(valid_email, valid_password) # запрос api -ключа и его сохранение в auth_key
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo) # добавление питомца
    assert status == 200
    print(f'Статус код: {status}, при добавлении питомца с текстом в поле "возраст"! ({age})')
    print(f'***Новый питомец: {status},\n{result}')


