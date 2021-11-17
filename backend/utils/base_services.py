from django.db import models
from django.shortcuts import get_object_or_404


class BaseService:
    """
    Базовый сервис с бизенес логикой для все приложений.
    """

    def __init__(self):
        self.instance: models.Model

    def get_all(self) -> models.Model:
        """
        Метод вернет список всех моделей экземпляра класса.
        :return: список моделей.
        """
        return self.instance.objects.all()

    def get_by_id(self, instance_id: int) -> models.Model:
        """
        :param instance_id: id экземпляра модели.
        :return: экземпляр модели найденный по id.
        """
        return get_object_or_404(self.instance, pk=instance_id)

    def create(self, data: dict):
        """
        Создаст экземпляр модели.
        В теле запроса передаются необходимые параметры модели.
        :return: возвращает новый экземпляр модели
        """
        new_instance = self.instance.objects.create(**data)
        return new_instance

    def update(self, updating_instance: models.Model, data: dict) -> models.Model:
        """
        Обновит сущетсвующий экземпляр модели.
        :param updating_instance: обновляемый экземпляр модели.
        :param data: новые данные для модели.
        :return: обновленный инстанс.
        """
        updated_instance = self.instance.objects.filter(id=updating_instance.id)
        updated_instance.update(**data)
        return updated_instance

    def delete(self, instance_id: str) -> bool:
        """
        Удалит существующий экземпляр модели.
        :param instance_id: id экземпляра модели.
        :return: Tru если удаление удачно и False если не сможет найти модель по такому id.
        """
        instance = get_object_or_404(self.instance, pk=instance_id)
        instance.delete()
        return True
