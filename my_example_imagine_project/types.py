import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import M1, M2


class M1Node(DjangoObjectType):

    class Meta:
        model = M1
        interfaces = (relay.Node, )
        fields = ['id', 'm2s']
        filter_fields = ['id', 'm2s']


class M2Node(DjangoObjectType):

    class Meta:
        model = M2
        interfaces = (relay.Node, )
        fields = ['id', 'm1s']
        filter_fields = ['id', 'm1s']
