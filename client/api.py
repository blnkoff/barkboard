import re
from typing import Self
from httpx import Response
from sensei import Router, APIModel, Query

router = Router('https://dog.ceo/api')

class Breed(APIModel):
    @classmethod
    @router.get("/breeds/list/all")
    def get_breeds(cls) -> dict[str, list[str]]:
        pass  
    
    @classmethod
    @get_breeds.finalize
    def _get_breeds_out(cls, response: Response) -> dict[str, list[str]]:
        """
        Обрабатывает ответ и возвращает словарь с породами.
        - response: HTTP-ответ от API.
        Возвращает словарь вида {'breed': ['sub-breed1', 'sub-breed2', ...]}.
        """
        data = response.json()
        return data["message"]


class DogImage(APIModel):
    url: str               # URL изображения
    breed: str             # основная порода
    sub_breed: str | None  # субпорода (если есть)

    @classmethod
    def _parse_url(cls, url: str) -> tuple[str, str | None]:
        """
        Извлекает породу и субпороду из URL.
        - url: полный URL, содержащий '/breeds/{slug}/'
        Возвращает (breed, sub_breed).
        """
        # Ищем сегмент 'breeds/{slug}/'
        m = re.search(r"/breeds/(?P<slug>[^/]+)/", url)
        if not m:
            return "", None
        slug = m.group("slug")
        # Делим по первому дефису
        parts = slug.split("-", 1)
        main = parts[0]
        sub = parts[1] if len(parts) == 2 else None
        return main, sub

    @classmethod
    def _out_image(cls, response: Response) -> Self:
        """Обрабатывает JSON и создаёт экземпляр с полями url, breed и sub_breed."""
        url = response.json()["message"]
        breed, sub_breed = cls._parse_url(url)
        return cls(url=url, breed=breed, sub_breed=sub_breed)

    @classmethod
    @router.get("/breeds/image/random")
    def _random(cls) -> Self:
        pass  # реализация генерируется Sensei

    @classmethod
    @_random.finalize
    def _random_out(cls, response: Response) -> Self:
        """Обработка ответа для случайного изображения."""
        return cls._out_image(response)

    @classmethod
    @router.get("/breed/{breed}/images/random")
    def _random_by_breed(cls, breed: str = Query()) -> Self:
        pass

    @classmethod
    @_random_by_breed.finalize
    def _random_by_breed_out(cls, response: Response) -> Self:
        """Обработка ответа для изображения по породе."""
        return cls._out_image(response)

    @classmethod
    def random(cls, breed: str | None = None) -> Self:
        """
        Если указан breed, вызывает _random_by_breed, иначе — _random.
        """
        if breed:
            return cls._random_by_breed(breed)
        return cls._random()
        