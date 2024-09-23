import boto3
from .utils import handle_aws_error


class Subscriber:
    def __init__(self, topic_manager):
        self.sns = boto3.client("sns")
        self.topic_manager = topic_manager

    @handle_aws_error
    def subscribe(self, topic_name, protocol, endpoint):
        topic_arn = self.topic_manager.get_topic_arn(topic_name)
        response = self.sns.subscribe(
            TopicArn=topic_arn, Protocol=protocol, Endpoint=endpoint
        )
        return response["SubscriptionArn"]

    @handle_aws_error
    def unsubscribe(self, subscription_arn):
        self.sns.unsubscribe(SubscriptionArn=subscription_arn)

    @handle_aws_error
    def list_subscriptions(self, topic_name=None):
        if topic_name:
            topic_arn = self.topic_manager.get_topic_arn(topic_name)
            response = self.sns.list_subscriptions_by_topic(TopicArn=topic_arn)
        else:
            response = self.sns.list_subscriptions()
        return response["Subscriptions"]
