class ListMixin:
    def list(self) -> dict:
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_data(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return serializer.data


class CreateMixin:
    def create(self) -> dict:
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class DestroyMixin:
    def destroy(self) -> bool:
        instance = self.get_object()
        instance.delete()
        return True


class RetrieveMixin:
    def retrieve(self, pk: int = None) -> dict:
        context = {self.lookup_field: pk} if pk is not None else None
        serializer = self.get_serializer(self.get_object(context))
        return serializer.data
