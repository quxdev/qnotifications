import unittest
from unittest.mock import patch, MagicMock
import json
import os
from qnotifications import SNSWrapper
from qnotifications.topics import TopicManager
from qnotifications.publishers import Publisher
from qnotifications.subscribers import Subscriber


class TestSNSWrapper(unittest.TestCase):
    def setUp(self):
        self.app_prefix = "testapp"
        self.persistence_file = "test_topic_mapping.json"

        # Ensure the persistence file doesn't exist before each test
        if os.path.exists(self.persistence_file):
            os.remove(self.persistence_file)

        self.patcher = patch("boto3.client")
        self.mock_boto_client = self.patcher.start()
        self.mock_sns = MagicMock()
        self.mock_boto_client.return_value = self.mock_sns

        # Instantiate SNSWrapper with persistence_file
        self.sns_wrapper = SNSWrapper(
            app_prefix=self.app_prefix,
            aws_access_key_id="test_key",
            aws_secret_access_key="test_secret",
            region_name="us-west-2",
            persistence_file=self.persistence_file,
        )

    def tearDown(self):
        self.patcher.stop()
        if os.path.exists(self.persistence_file):
            os.remove(self.persistence_file)

    def test_create_topic(self):
        topic_name = "test-topic"
        self.mock_sns.create_topic.return_value = {
            "TopicArn": f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        }

        result = self.sns_wrapper.create_topic(topic_name)

        self.assertEqual(result, topic_name)
        self.mock_sns.create_topic.assert_called_once_with(
            Name=f"{self.app_prefix}-{topic_name}"
        )

    def test_create_duplicate_topic(self):
        topic_name = "test-topic"
        self.mock_sns.create_topic.return_value = {
            "TopicArn": f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        }

        self.sns_wrapper.create_topic(topic_name)

        with self.assertRaises(ValueError):
            self.sns_wrapper.create_topic(topic_name)

    def test_delete_topic(self):
        topic_name = "test-topic"
        topic_arn = f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        self.sns_wrapper.topic_manager.topic_map[topic_name] = topic_arn

        self.sns_wrapper.delete_topic(topic_name)

        self.mock_sns.delete_topic.assert_called_once_with(TopicArn=topic_arn)
        self.assertNotIn(topic_name, self.sns_wrapper.topic_manager.topic_map)

    def test_list_topics(self):
        self.mock_sns.list_topics.return_value = {
            "Topics": [
                {
                    "TopicArn": f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-topic1"
                },
                {
                    "TopicArn": f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-topic2"
                },
                {"TopicArn": "arn:aws:sns:us-west-2:123456789012:other-app-topic"},
            ]
        }

        result = self.sns_wrapper.list_topics()

        self.assertEqual(set(result), {"topic1", "topic2"})

    def test_publish(self):
        topic_name = "test-topic"
        topic_arn = f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        message = "Test message"
        self.sns_wrapper.topic_manager.topic_map[topic_name] = topic_arn
        self.mock_sns.publish.return_value = {"MessageId": "test-message-id"}

        result = self.sns_wrapper.publish(topic_name, message)

        self.assertEqual(result, "test-message-id")
        self.mock_sns.publish.assert_called_once_with(
            TopicArn=topic_arn, Message=message
        )

    def test_subscribe(self):
        topic_name = "test-topic"
        topic_arn = f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        protocol = "email"
        endpoint = "test@example.com"
        self.sns_wrapper.topic_manager.topic_map[topic_name] = topic_arn
        self.mock_sns.subscribe.return_value = {
            "SubscriptionArn": "test-subscription-arn"
        }

        result = self.sns_wrapper.subscribe(topic_name, protocol, endpoint)

        self.assertEqual(result, "test-subscription-arn")
        self.mock_sns.subscribe.assert_called_once_with(
            TopicArn=topic_arn, Protocol=protocol, Endpoint=endpoint
        )

    def test_unsubscribe(self):
        subscription_arn = "test-subscription-arn"

        self.sns_wrapper.unsubscribe(subscription_arn)

        self.mock_sns.unsubscribe.assert_called_once_with(
            SubscriptionArn=subscription_arn
        )

    def test_list_subscriptions(self):
        topic_name = "test-topic"
        topic_arn = f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        self.sns_wrapper.topic_manager.topic_map[topic_name] = topic_arn
        self.mock_sns.list_subscriptions_by_topic.return_value = {
            "Subscriptions": [
                {
                    "SubscriptionArn": "arn1",
                    "Protocol": "email",
                    "Endpoint": "test1@example.com",
                },
                {
                    "SubscriptionArn": "arn2",
                    "Protocol": "sms",
                    "Endpoint": "+1234567890",
                },
            ]
        }

        result = self.sns_wrapper.list_subscriptions(topic_name)

        self.assertEqual(len(result), 2)
        self.mock_sns.list_subscriptions_by_topic.assert_called_once_with(
            TopicArn=topic_arn
        )

    def test_persistence(self):
        topic_name = "test-topic"
        topic_arn = f"arn:aws:sns:us-west-2:123456789012:{self.app_prefix}-{topic_name}"
        self.mock_sns.create_topic.return_value = {"TopicArn": topic_arn}

        self.sns_wrapper.create_topic(topic_name)

        # Create a new SNSWrapper instance to test if the topic mapping is loaded from the file
        new_sns_wrapper = SNSWrapper(
            app_prefix=self.app_prefix, persistence_file=self.persistence_file
        )

        self.assertIn(topic_name, new_sns_wrapper.topic_manager.topic_map)
        self.assertEqual(new_sns_wrapper.topic_manager.topic_map[topic_name], topic_arn)


if __name__ == "__main__":
    unittest.main()
