import unittest
from mock import Mock
from testfixtures import compare
from testfixtures import Replacer

import os

import yaml

from deployfish.aws.ecs import Service


class TestService_load_yaml(unittest.TestCase):

    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        fname = os.path.join(current_dir, 'simple.yml')
        with open(fname) as f:
            yml = yaml.load(f)

        # service_client = Mock()
        # service_client.describe_services = Mock(return_value={'services':[]})
        # client = Mock(return_value=service_client)
        with Replacer() as r:
            # r.replace('boto3.client', client)
            # r.replace('deployfish.aws.ecs.Service.__get_service', Mock(return_value={}), strict=False)
            r.replace('deployfish.aws.ecs.Service.from_aws', Mock())
            self.service = Service(yml=yml['services'][0])

    def test_serviceName(self):
        self.assertEqual(self.service.serviceName, 'foobar-prod')

    def test_clusterName(self):
        self.assertEqual(self.service.clusterName, 'access-caltech-proxy-prod')

    def test_roleArn(self):
        self.assertEqual(self.service.roleArn, 'a_task_role_arn')

    def test_count(self):
        self.assertEqual(self.service.count, 2)

    def test_load_balancer(self):
        compare(self.service.load_balancer, {
            'type': 'elb',
            'load_balancer_name': 'access-caltech-proxy-prod',
            'container_name': 'cit_auth',
            'container_port': 443
        })
