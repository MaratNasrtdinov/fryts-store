from models import *
def update_price_past_dict(message=None, callback=None):
    price_past_dict = {
        Catalog.get(Catalog.id == 1).name : {'Количество': Catalog.get(Catalog.id == 1).quantity, 'Цена': Catalog.get(Catalog.id == 1).price,
                                             'Имя': Catalog.get(Catalog.id == 1).name, 'Позиция': 1, 'Описание': Catalog.get(Catalog.id == 1).description},
        Catalog.get(Catalog.id == 2).name : {'Количество': Catalog.get(Catalog.id == 2).quantity, 'Цена': Catalog.get(Catalog.id == 2).price,
                                             'Имя': Catalog.get(Catalog.id == 2).name, 'Позиция': 2, 'Описание': Catalog.get(Catalog.id == 2).description},
        Catalog.get(Catalog.id == 3).name : {'Количество': Catalog.get(Catalog.id == 3).quantity, 'Цена': Catalog.get(Catalog.id == 3).price,
                                             'Имя': Catalog.get(Catalog.id == 3).name, 'Позиция': 3, 'Описание': Catalog.get(Catalog.id == 3).description},
        Catalog.get(Catalog.id == 4).name : {'Количество': Catalog.get(Catalog.id == 4).quantity, 'Цена': Catalog.get(Catalog.id == 4).price,
                                             'Имя': Catalog.get(Catalog.id == 4).name, 'Позиция': 4, 'Описание': Catalog.get(Catalog.id == 4).description},
        Catalog.get(Catalog.id == 5).name : {'Количество': Catalog.get(Catalog.id == 5).quantity, 'Цена': Catalog.get(Catalog.id == 5).price,
                                             'Имя': Catalog.get(Catalog.id == 5).name, 'Позиция': 5, 'Описание': Catalog.get(Catalog.id == 5).description},
        Catalog.get(Catalog.id == 6).name : {'Количество': Catalog.get(Catalog.id == 6).quantity, 'Цена': Catalog.get(Catalog.id == 6).price,
                                             'Имя': Catalog.get(Catalog.id == 6).name, 'Позиция': 6, 'Описание': Catalog.get(Catalog.id == 6).description},
        Catalog.get(Catalog.id == 7).name : {'Количество': Catalog.get(Catalog.id == 7).quantity, 'Цена': Catalog.get(Catalog.id == 7).price,
                                             'Имя': Catalog.get(Catalog.id == 7).name, 'Позиция': 7, 'Описание': Catalog.get(Catalog.id == 7).description}
    }
    return price_past_dict
def update_price_past_list(message=None, callback=None):
    price_past_dict = update_price_past_dict()
    price_past = list(price_past_dict.keys())

    return price_past

update_price_past_dict()


