from .topics import TopicManager
from .publishers import Publisher
from .subscribers import Subscriber, PersistentSubscriber
from .utils import configure_aws_credentials


class SNSWrapper:
    def __init__(self, app_prefix, aws_access_key_id=None, aws_secret_access_key=None, region_name=None):
        configure_aws_credentials(aws_access_key_id, aws_secret_access_key, region_name)
        self.topic_manager = TopicManager(app_prefix)
        self.subscriber = PersistentSubscriber(self.topic_manager)
        self.publisher = Publisher(self.topic_manager)
        self.system_topic = self.topic_manager.create_topic("_newtopic")
        self.subscribe(self.system_topic, None,None)
        self.subscriber.subscribe_to_all_topics()

    def create_topic(self, name):
        if name not in self.list_topics() and not name == self.system_topic:
            topic = self.topic_manager.create_topic(name)
            self.publish(self.system_topic, name)
            return topic
        return None

    def publish(self, topic_name, message):
        return self.publisher.publish(topic_name, message)

    def subscribe(self, topic_name, protocol, endpoint):
        return self.subscriber.subscribe(topic_name, protocol, endpoint)

    def unsubscribe(self, subscription_arn):
        self.subscriber.unsubscribe(subscription_arn)

    def list_topics(self):
        return self.topic_manager.list_topics()

    def list_subscriptions(self, topic_name=None):
        return self.subscriber.list_subscriptions(topic_name)

    def delete_topic(self, topic_arn):
        self.topic_manager.delete_topic(topic_arn)

    def get_topic_arn(self, topic_name):
        return self.topic_manager.get_topic_arn(topic_name)


    def get_messages(self, topic=None, start_datetime=None):
        return self.subscribe.get_messages(topic, start_datetime)

__all__ = ["SNSWrapper", "TopicManager", "Publisher", "Subscriber"]
