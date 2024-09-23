# test_qnotifications.py
from qnotifications import SNSWrapper

# Replace these with your actual AWS credentials
aws_access_key_id = None
aws_secret_access_key = None
region_name = 'us-west-2'
app_prefix = 'my-app'  # Add your application prefix here

# Initialize the SNSWrapper
sns = SNSWrapper(app_prefix=app_prefix, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=region_name)

# Create a topic
topic_arn = sns.create_topic('my-test-topic')
print(f"Created topic ARN: {topic_arn}")

# Publish a message
message_id = sns.publish('my-test-topic', 'Hello, World!')
print(f"Published message ID: {message_id}")

# Subscribe to the topic using topic name
subscription_arn = sns.subscribe('my-test-topic', 'email', 'psathaye@gmail.com')
print(f"Subscription ARN: {subscription_arn}")

# List topics
topics = sns.list_topics()
print(f"Topics: {topics}")

# List subscriptions
subscriptions = sns.list_subscriptions('my-test-topic')
print(f"Subscriptions: {subscriptions}")

# Unsubscribe if the subscription is confirmed
if subscription_arn != 'PendingConfirmation':
    sns.unsubscribe(subscription_arn)
    print(f"Unsubscribed from: {subscription_arn}")
else:
    print(f"Subscription {subscription_arn} is still pending confirmation")

# Delete the topic
sns.delete_topic(topic_arn)
print(f"Deleted topic ARN: {topic_arn}")