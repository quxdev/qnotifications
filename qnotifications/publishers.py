import boto3
from .utils import handle_aws_error


class Publisher:
    def __init__(self, topic_manager):
        self.sns = boto3.client("sns")
        self.topic_manager = topic_manager

    @handle_aws_error
    def publish(self, topic_name, message):
        topic_arn = self.topic_manager.get_topic_arn(topic_name)
        response = self.sns.publish(TopicArn=topic_arn, Message=message)
        return response["MessageId"]
