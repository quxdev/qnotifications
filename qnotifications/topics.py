import os
import json
import boto3
from .utils import handle_aws_error


class TopicManager:
    def __init__(self, app_prefix, persistence_file="topic_mapping.json"):
        self.sns = boto3.client("sns")
        self.app_prefix = app_prefix
        self.persistence_file = persistence_file
        self.topic_map = self.load_topic_map()

    def load_topic_map(self):
        if os.path.exists(self.persistence_file):
            with open(self.persistence_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_topic_map(self):
        with open(self.persistence_file, "w", encoding="utf-8") as f:
            json.dump(self.topic_map, f)

    def get_prefixed_name(self, name):
        return f"{self.app_prefix}-{name}"

    def topic_exists(self, name):
        return name in self.topic_map

    @handle_aws_error
    def create_topic(self, name):
        if self.topic_exists(name):
            raise ValueError(f"Topic '{name}' already exists in this application")

        prefixed_name = self.get_prefixed_name(name)
        response = self.sns.create_topic(Name=prefixed_name)
        arn = response["TopicArn"]
        self.topic_map[name] = arn
        self.save_topic_map()
        return name

    @handle_aws_error
    def delete_topic(self, name):
        arn = self.topic_map.get(name)
        if arn:
            self.sns.delete_topic(TopicArn=arn)
            del self.topic_map[name]
            self.save_topic_map()
        else:
            raise ValueError(f"Topic '{name}' not found")

    @handle_aws_error
    def list_topics(self):
        response = self.sns.list_topics()
        aws_topics = {
            arn.split(":")[-1]: arn
            for arn in [topic["TopicArn"] for topic in response["Topics"]]
        }

        # Update topic_map with any topics created outside this wrapper
        for prefixed_name, arn in aws_topics.items():
            if prefixed_name.startswith(self.app_prefix):
                name = prefixed_name[len(self.app_prefix) + 1 :]
                if name not in self.topic_map:
                    self.topic_map[name] = arn

        # Remove any topics that no longer exist in AWS
        self.topic_map = {
            name: arn
            for name, arn in self.topic_map.items()
            if arn in aws_topics.values()
        }

        self.save_topic_map()
        return list(self.topic_map.keys())

    def get_topic_arn(self, name):
        arn = self.topic_map.get(name)
        if not arn:
            raise ValueError(f"Topic '{name}' not found")
        return arn
