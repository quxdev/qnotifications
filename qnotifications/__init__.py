from .topics import TopicManager
from .publishers import Publisher
from .subscribers import Subscriber
from .utils import configure_aws_credentials


class SNSWrapper:
    def __init__(
        self,
        app_prefix,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        region_name=None,
        persistence_file="topic_mapping.json",
    ):
        configure_aws_credentials(aws_access_key_id, aws_secret_access_key, region_name)
        self.topic_manager = TopicManager(app_prefix, persistence_file)
        self.publisher = Publisher(self.topic_manager)
        self.subscriber = Subscriber(self.topic_manager)

    def create_topic(self, name):
        return self.topic_manager.create_topic(name)

    def delete_topic(self, name):
        return self.topic_manager.delete_topic(name)

    def list_topics(self):
        return self.topic_manager.list_topics()

    def publish(self, topic_name, message):
        return self.publisher.publish(topic_name, message)

    def subscribe(self, topic_name, protocol, endpoint):
        return self.subscriber.subscribe(topic_name, protocol, endpoint)

    def unsubscribe(self, subscription_arn):
        return self.subscriber.unsubscribe(subscription_arn)

    def list_subscriptions(self, topic_name=None):
        return self.subscriber.list_subscriptions(topic_name)

    def get_topic_arn(self, topic_name):
        topics = self.list_topics()
        for topic in topics:
            if topic_name in topic['TopicArn']:
                return topic['TopicArn']
        raise ValueError(f"Topic '{topic_name}' not found")

    def subscribe_by_name(self, topic_name, protocol, endpoint):
        topic_arn = self.get_topic_arn(topic_name)
        return self.subscribe(topic_arn, protocol, endpoint)


__all__ = ["SNSWrapper", "TopicManager", "Publisher", "Subscriber"]
