import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from my_example_imagine_project.models import M1
from my_example_imagine_project.types import M1Node


class M1CreateData(graphene.InputObjectType):

    m2s = graphene.List(graphene.NonNull(graphene.ID), default_value=[])


class CreateM1(relay.ClientIDMutation):
    class Input:
        data = M1CreateData()

    m1 = graphene.Field(M1Node)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data):

        m2s = data.pop('m2s', [])

        obj = M1.objects.create(**data)

        m2s_pks = list(map(lambda m2s_id: from_global_id(m2s_id)[1], m2s))
        obj.m2s.set(m2s_pks)

        return CreateM1(m1=obj)


class DeleteM1(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = M1.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteM1(ok=True)
