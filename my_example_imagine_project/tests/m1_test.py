import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from my_example_imagine_project.models import M1
from my_example_imagine_project.types import M1Node, M2Node

from .factories import M1Factory, M2Factory

faker = Factory.create()


class M1_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        M1Factory.create_batch(size=3)

    def test_create_m1(self):
        """
        Ensure we can create a new m1 object.
        """

        m1_dict = camelize(factory.build(dict, FACTORY_CLASS=M1Factory))

        response = self.query(
            """
            mutation($input: CreateM1Input!) {
                createM1(input: $input) {
                    clientMutationId,
                    m1 {
                        id
                    }
                }
            }
            """,
            input_data={'data': m1_dict}
        )
        content = json.loads(response.content)
        generated_m1 = content['data']['createM1']['m1']
        self.assertResponseNoErrors(response)

    def test_create_m1_w_m2m_relation(self):
        """
        Ensure we can create a new m1 object with its many to many relations.
        """

        m2s = M2Factory.create_batch(size=3)
        m2s_ids = list(map(lambda single_m2s: to_global_id(M2Node._meta.name, single_m2s.pk), m2s))

        m1_dict = camelize(factory.build(dict, FACTORY_CLASS=M1Factory, m2s=m2s_ids))

        response = self.query(
            """
            mutation($input: CreateM1Input!) {
                createM1(input: $input) {
                    clientMutationId,
                    m1 {
                        id
                        m2s {
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
            input_data={'data': m1_dict}
        )
        content = json.loads(response.content)
        generated_m1 = content['data']['createM1']['m1']
        self.assertResponseNoErrors(response)
        generated_m2s = generated_m1['m2s']['edges']
        self.assertEquals(len(m2s_ids), len(generated_m2s))

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allM1 query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allM1{
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
        m1s = content['data']['allM1']['edges']
        m1s_qs = M1.objects.all()
        for i, edge in enumerate(m1s):
            m1 = edge['node']
            self.assertEquals(m1['id'], to_global_id(M1Node._meta.name, m1s_qs[i].id))

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allM1 query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allM1{
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
        m1s = content['data']['allM1']['edges']
        m1_count = len(m1s)
        for i, edge in enumerate(m1s, start=1):
            m1 = edge['node']
            m1_id = m1['id']
            response = self.query(
                """
                mutation($input:DeleteM1Input!) {
                   deleteM1(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': m1_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            m1s = content['data']['allM1']['edges']
            new_len = len(m1s)
            assert m1_count - i == new_len

    def test_update_m1_w_m2m_relation(self):
        """
        Ensure we can update an m1 object and add interpreters to it.
        """
        m2s = M2Factory.create_batch(size=3)
        m2s_ids = list(map(lambda single_m2s: to_global_id(M2Node._meta.name, single_m2s.pk), m2s))

        m1 = M1Factory.create()
        m1_id = to_global_id(M1Node._meta.name, m1.pk)

        response = self.query(
            """
            mutation($input: UpdateM1Input!){
                updateM1(input: $input) {
                    m1{
                        m2s {
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
                'id': m1_id,
                'data': {
                    'm2s': m2s_ids,
                }
            }
        )
        content = json.loads(response.content)
        generated_m1 = content['data']['updateM1']['m1']
        self.assertResponseNoErrors(response)
        generated_m2s = generated_m1['m2s']['edges']
        self.assertEquals(len(m2s_ids), len(generated_m2s))
