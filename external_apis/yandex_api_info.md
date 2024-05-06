### Ответ Яндекса при поиске организаций    

Корневой элемент - "FeatureCollection".

    
В "properties" содержатся метаданные запроса и ответа.

        "ResponseMetaData" содержит информацию о запросе и ответе.
            "SearchRequest" содержит информацию о запросе.
                "request" - текст запроса.
                "results" - максимальное количество возвращаемых результатов.
                "skip" - количество пропускаемых результатов.
                "boundedBy" - границы области, в которой предположительно находятся искомые объекты.
            "SearchResponse" содержит информацию о самом ответе.
                "found" - количество найденных объектов.
                "boundedBy" - границы области показа найденных объектов.
                "display" - рекомендации по отображению результатов поиска.
    
"features" содержит список найденных объектов.

        Каждый объект представлен в формате "Feature".
            "properties" содержит информацию о найденном объекте.
                "CompanyMetaData" содержит сведения об организации.
                    "id", "name", "address", "url" - основная информация об организации.
                    "Categories" - список категорий, к которым принадлежит организация.
                    "Hours" - режим работы организации.
                "description" - текст, который рекомендуется указывать в качестве подзаголовка при отображении найденной организации.
                "name" - текст, который рекомендуется указывать в качестве заголовка при отображении найденной организации.
            "geometry" содержит информацию о геометрии найденного объекта.
                "type" - тип геометрии (в данном случае "Point").
                "coordinates" - координаты организации в формате "долгота, широта".