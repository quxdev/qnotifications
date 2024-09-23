import datetime
import json
import boto3
from .utils import handle_aws_error
from dotenv import load_dotenv
import os

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

class PersistentSubscriber(Subscriber):
    def __init__(self, topic_manager):
        load_dotenv()  # Load environment variables from .env file
        self.storage_file = os.getenv("STORAGE_FILE", "all_messages.json")  # Default to "all_messages.json"
        super().__init__(topic_manager=topic_manager)

    def subscribe_to_all_topics(self):
        for topic in self.topic_manager.get_all_topics():
            self.subscribe(topic)
        
    def on_message(self, topic, message):
        if topic == "_newtopic":
            self.subscribe(message)
        else:
            self.save_message(topic, message)
    
    def save_message(self, topic, message):
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "topic": topic,
            "message": message
        }
        with open(self.storage_file, 'a') as f:
            json.dump(entry, f)
            f.write('\n')

    def get_messages(self, topic=None, start_datetime=None):
        messages = []
        with open(self.storage_file, 'r') as f:
            for line in f:
                entry = json.loads(line)
                if (topic is None or entry['topic'] == topic) and \
                    (start_datetime is None or entry['timestatmp'] >= start_datetime):
                    messages.append(entry)
        return messages
