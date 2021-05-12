from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from my_example_imagine_project.models import M1, M2

faker = Factory.create()


class M1Factory(DjangoModelFactory):
    class Meta:
        model = M1


class M2Factory(DjangoModelFactory):
    class Meta:
        model = M2
