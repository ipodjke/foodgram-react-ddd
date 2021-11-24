from rest_framework.filters import SearchFilter


class DoubleSearchBackend(SearchFilter):
    """
    Бекенд для фильтрации с выводом в заданой последовательности.

    Поддерживает примущества базавого фильтра, но выводит
    результаты в последовательности указанной в search_fields
    """
    def filter_queryset(self, request, queryset, view):
        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(str(search_field))
            for search_field in search_fields
        ]

        filtered_queryset = []
        for search_term in search_terms:
            for orm_lookup in orm_lookups:
                ingredients = (queryset.filter(
                    **{orm_lookup: search_term}
                ))
                for ingredient in ingredients:
                    if ingredient not in filtered_queryset:
                        filtered_queryset.append(ingredient.id)
        return queryset.filter(id__in=filtered_queryset)
