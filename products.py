from enum import Enum

class ProductCollection:

    def __init__(self):

        self._products = []

    def add(self, product):
        if isinstance(product, list):
            self._products += product
        else:
            self._products.append(product)

    def get_possible_produced(ztype):
        return filter(lambda p: p.has_producer(ztype), self._products)

    def get_possible_consumed(ztype):
        return filter(lambda p: p.has_consumer(ztype), self._products)


class Product:

    def __init__(self, name, producers):

        self._name = name
        self._producers = producers

        if not isinstance(self._producers, list):
            self._producers = [self._producers]

    def get_name(self):
        return self._name

    def get_producers(self):
        return self._producers

    def has_producer(self, ztype):
        return (ztype in self._producers)



