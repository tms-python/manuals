import json
from abc import ABC, abstractmethod
#  Factory Method


class AbstractSerializer(ABC):
    @abstractmethod
    def serialize(self, data):
        pass


class JsonSerializer(AbstractSerializer):
    def serialize(self, data):
        return json.dumps(data)


class YamlSerializer(AbstractSerializer):
    def serialize(self, data):
        return data


class XmlSerializer(AbstractSerializer):
    @staticmethod
    def wrap_data(response: str, tag: str, value: str):
        return f'{response}\n<{tag}>\n\t{value}\n</{tag}>\n'

    def serialize(self, data: dict):
        response_in_xml = '<?xml version="1.1" encoding="UTF-8"?>'
        for name, value in data.items():
            response_in_xml = self.wrap_data(response_in_xml, name, value)
        return response_in_xml


data_for_serialize = {'id': 1, 'name': 'some_name', 'type': 'some_type'}


class Serializer:
    __serializer = None

    #  при инициализации передается тип данных в который нам нужно преобразовать словарь
    def __init__(self, serializer_type: str):
        # вызывается метод для получения сериализатора в переданный тип данных
        self.get_serializer(serializer_type=serializer_type)

    def get_serializer(self, serializer_type: str):
        #  в зависимости от типа данных, в self.__serializer записывается требуемый сериализатор
        if serializer_type == 'json':
            self.__serializer = JsonSerializer()
        elif serializer_type == 'xml':
            self.__serializer = XmlSerializer()
        elif serializer_type == 'yaml':
            self.__serializer = YamlSerializer()
        else:
            raise TypeError(f'{serializer_type} type for serializing not defined')

    # метод принимающий данные и сериализующий их с помощью полученного сериализатора
    def serialize_data(self, data: dict) -> str:
        return self.__serializer.serialize(data)


serializer = Serializer('json')
print(serializer.serialize_data(data_for_serialize), '\n')

serializer = Serializer('xml')
print(serializer.serialize_data(data_for_serialize))

serializer = Serializer('yaml')
print(serializer.serialize_data(data_for_serialize))


"""
yaml
containers:
  - name: nginx-container
    image: nginx
json
{
  "apiVersion": "apps/v1", 
  "containers": [
      {"name": "nginx-container"}, 
      {"image": "nginx"}
    ]
}
"""

def serializer(data, type_serialized_data):
    if type_serialized_data == 'json':
        pass
    elif type_serialized_data == 'xml':
        pass