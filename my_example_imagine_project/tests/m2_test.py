import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from my_example_imagine_project.models import M2
from my_example_imagine_project.types import M1Node, M2Node

from .factories import M1Factory, M2Factory

faker = Factory.create()


class M2_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        M2Factory.create_batch(size=3)

    def test_create_m2(self):
        """
        Ensure we can create a new m2 object.
        """

        m2_dict = camelize(factory.build(dict, FACTORY_CLASS=M2Factory))

        response = self.query(
            """
            mutation($input: CreateM2Input!) {
                createM2(input: $input) {
                    clientMutationId,
                    m2 {
                        id
                    }
                }
            }
            """,
            input_data={'data': m2_dict}
        )
        content = json.loads(response.content)
        generated_m2 = content['data']['createM2']['m2']
        self.assertResponseNoErrors(response)

    def test_create_m2_w_m2m_relation(self):
        """
        Ensure we can create a new m2 object with its many to many relations.
        """

        m1s = M1Factory.create_batch(size=3)
        m1s_ids = list(map(lambda single_m1s: to_global_id(M1Node._meta.name, single_m1s.pk), m1s))

        m2_dict = camelize(factory.build(dict, FACTORY_CLASS=M2Factory, m1s=m1s_ids))

        response = self.query(
            """
            mutation($input: CreateM2Input!) {
                createM2(input: $input) {
                    clientMutationId,
                    m2 {
                        id
                        m1s {
                            edges{
                                node{
                                    id
                                }
                            }
                        }
                    }
                }
            }
            """,
            input_data={'data': m2_dict}
        )
        content = json.loads(response.content)
        generated_m2 = content['data']['createM2']['m2']
        self.assertResponseNoErrors(response)
        generated_m1s = generated_m2['m1s']['edges']
        self.assertEquals(len(m1s_ids), len(generated_m1s))

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allM2 query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allM2{
                    edges{
                        node{
                            id
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        m2s = content['data']['allM2']['edges']
        m2s_qs = M2.objects.all()
        for i, edge in enumerate(m2s):
            m2 = edge['node']
            self.assertEquals(m2['id'], to_global_id(M2Node._meta.name, m2s_qs[i].id))

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allM2 query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allM2{
                    edges{
                        node{
                            id
                        }
                    }
                }
            }
            """
        response = self.query(list_query)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        m2s = content['data']['allM2']['edges']
        m2_count = len(m2s)
        for i, edge in enumerate(m2s, start=1):
            m2 = edge['node']
            m2_id = m2['id']
            response = self.query(
                """
                mutation($input:DeleteM2Input!) {
                   deleteM2(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': m2_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            m2s = content['data']['allM2']['edges']
            new_len = len(m2s)
            assert m2_count - i == new_len

    def test_update_m2_w_m2m_relation(self):
        """
        Ensure we can update an m2 object and add interpreters to it.
        """
        m1s = M1Factory.create_batch(size=3)
        m1s_ids = list(map(lambda single_m1s: to_global_id(M1Node._meta.name, single_m1s.pk), m1s))

        m2 = M2Factory.create()
        m2_id = to_global_id(M2Node._meta.name, m2.pk)

        response = self.query(
            """
            mutation($input: UpdateM2Input!){
                updateM2(input: $input) {
                    m2{
                        m1s {
                            edges{
                                node{
                                    id
                                }
                            }
                        }
                    }
                }
            }
            """,
            input_data={
                'id': m2_id,
                'data': {
                    'm1s': m1s_ids,
                }
            }
        )
        content = json.loads(response.content)
        generated_m2 = content['data']['updateM2']['m2']
        self.assertResponseNoErrors(response)
        generated_m1s = generated_m2['m1s']['edges']
        self.assertEquals(len(m1s_ids), len(generated_m1s))
