import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from my_example_imagine_project.models import M2
from my_example_imagine_project.types import M2Node


class M2CreateData(graphene.InputObjectType):

    m1s = graphene.List(graphene.NonNull(graphene.ID), default_value=[])


class CreateM2(relay.ClientIDMutation):
    class Input:
        data = M2CreateData()

    m2 = graphene.Field(M2Node)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data):

        m1s = data.pop('m1s', [])

        obj = M2.objects.create(**data)

        m1s_pks = list(map(lambda m1s_id: from_global_id(m1s_id)[1], m1s))
        obj.m1s.set(m1s_pks)

        return CreateM2(m2=obj)


class DeleteM2(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = M2.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteM2(ok=True)
