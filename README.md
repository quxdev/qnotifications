# QNotifications

QNotifications is a Python module that wraps around AWS SNS (Simple Notification Service) and simplifies its integration for various applications. It provides an easy-to-use interface for managing topics, publishing messages, and handling subscriptions.

## Features

- Simple topic management (create, delete, list)
- Easy publishing to topics
- Subscription management (subscribe, unsubscribe, list)
- Automatic handling of AWS credentials
- Error handling and retries
- Application-specific topic prefixing to avoid naming conflicts
- Persistence of topic mappings across sessions

## Installation

```
pip install qnotifications
```

## Usage

```python
from qnotifications import SNSWrapper

# Initialize the wrapper
sns = SNSWrapper(aws_access_key_id='YOUR_ACCESS_KEY', aws_secret_access_key='YOUR_SECRET_KEY', region_name='us-west-2')

# Create a topic
topic_arn = sns.create_topic('my-topic')

# Publish a message
message_id = sns.publish(topic_arn, 'Hello, World!')

# Subscribe to a topic using topic ARN
subscription_arn = sns.subscribe(topic_arn, 'email', 'psathaye@gmail.com')

# Subscribe to a topic using topic name
subscription_arn = sns.subscribe_by_name('my-topic', 'email', 'psathaye@gmail.com')

# List topics
topics = sns.list_topics()

# List subscriptions
subscriptions = sns.list_subscriptions(topic_arn)

# Unsubscribe
sns.unsubscribe(subscription_arn)

# Delete a topic
sns.delete_topic(topic_arn)
```

## Available Subscription Protocols and Their Requirements

When subscribing to a topic, you can use the following protocols. Some protocols require additional configuration:

1. `http`: Deliver messages via HTTP POST
   - Requires a publicly accessible HTTP endpoint

2. `https`: Deliver messages via HTTPS POST
   - Requires a publicly accessible HTTPS endpoint
   - The endpoint must have a valid SSL certificate

3. `email`: Deliver messages via email (text format)
   - Requires email address confirmation before messages are sent
   - Limited to 150 KB in size

4. `email-json`: Deliver messages via email (JSON format)
   - Requires email address confirmation before messages are sent
   - Can send larger messages compared to plain email protocol

5. `sms`: Deliver messages via SMS text message
   - Phone number must be in E.164 format
   - Message size limited to 140 bytes
   - Requires SMS permissions in your AWS account

6. `sqs`: Deliver messages to an Amazon SQS queue
   - Requires an existing SQS queue
   - The queue must grant the SNS service permission to send messages

7. `application`: Deliver messages to a mobile app and device
   - Requires setting up platform application endpoints (e.g., for iOS, Android)
   - Need to register the mobile app with AWS SNS first

8. `lambda`: Deliver messages to an AWS Lambda function
   - Requires an existing Lambda function
   - The Lambda function must grant the SNS service permission to invoke it

For `email` and `email-json` protocols:
- After subscribing, AWS SNS sends a confirmation email to the provided address
- The subscription is pending until the recipient confirms by clicking the link in the email
- You may need to check spam folders for the confirmation email

For `https` protocol:
- The HTTPS endpoint must respond to the subscription confirmation request
- Implement a route in your application to handle the `SubscriptionConfirmation` message type

For `application` protocol:
- You need to create a platform application in SNS for each platform (iOS, Android, etc.)
- Obtain and provide the necessary credentials (e.g., API key for Android, certificate for iOS)
- Register each device and obtain a device token
- Use the device token when subscribing to the topic

Note: Some protocols may have limitations or additional costs associated with them. Always refer to the latest AWS SNS documentation for the most up-to-date information on protocol-specific requirements and limitations.

## License

This project is licensed under the MIT License.
