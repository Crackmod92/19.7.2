import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder


class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"

    def get_api_key(self, email: str, password: str) -> json:
        """Метод осуществляет запрос к API сервера, возвращает статус запроса и результат формата json с уникальным ключем пользователя,
         найденного по заданным email и password"""

        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def get_list_of_pets(self, auth_key: json, filter: str="") -> json:
        """Метод осуществляет запрос к API сервера, возвращает статус запроса и список домашних животных
         (совпадающих с фильтром: пустой фильтр - все питомцы, фильтр my_pets - список питомцев пользователя) в формате json"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}

        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str, pet_photo: str) -> json:  #POST
        """Метод осуществляект post-запрос на сервер с данными о добавляемом питомце и возвращает статус
         запроса на сервер и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def delete_pet(self, auth_key: json, pet_id: str) -> json:  #DELETE
        """Метод осуществляект delete-запрос на сервер с id удаляемого питомца и возвращает статус
         запроса на сервер и результат в формате JSON с тескстом об удалении"""
        headers = {'auth_key': auth_key['key']}
        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result


    def update_pet_info(self, auth_key: json, pet_id: str, name: str, animal_type: str, age: int) -> json:     #PUT
        """Метод осуществляект put-запрос на сервер с id измемяемого питомца и возвращает статус
         запроса на сервер и результат в формате JSON с данными обновленного питомца"""
        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }
        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result

#Найти методы, которые ещё не реализованы в библиотеке, и написать их реализацию

    def add_new_pet_without_photo(self, auth_key: json, name: str, animal_type: str, age: str) ->json:
        """Метод осуществляект post-запрос на сервер с данными о добавляемом питомце (БЕЗ ФОТО) и возвращает статус
                запроса на сервер и результат в формате JSON с данными добавленного питомца (БЕЗ ФОТО)"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result


    def add_photo_of_a_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод осуществляект post-запрос на сервер с id о питомце, которому необходимо добавить фото и возвращает статус
            запроса на сервер и результат в формате JSON с данными питомца, которому добавлено фото"""
        data = MultipartEncoder(
            fields={
                #'pet_id': pet_id,
                'pet_photo':  (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
