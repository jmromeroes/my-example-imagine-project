from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations.m1 import CreateM1, DeleteM1
from .mutations.m2 import CreateM2, DeleteM2
from .types import M1Node, M2Node


class Query(ObjectType):
    m2 = relay.Node.Field(M2Node)
    m1 = relay.Node.Field(M1Node)

    all_m2 = DjangoFilterConnectionField(M2Node)
    all_m1 = DjangoFilterConnectionField(M1Node)


class Mutation(ObjectType):
    create_m2 = CreateM2.Field()
    create_m1 = CreateM1.Field()

    delete_m2 = DeleteM2.Field()
    delete_m1 = DeleteM1.Field()
