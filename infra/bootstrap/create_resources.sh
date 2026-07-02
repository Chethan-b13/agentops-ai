#!/bin/bash

set -e

echo "Creating SQS queue..."

aws --endpoint-url=http://localhost:4566 \
    sqs create-queue \
    --queue-name incident-events

echo "Creating EventBridge rule..."

aws --endpoint-url=http://localhost:4566 \
    events put-rule \
    --name cloudwatch-alarm-rule \
    --event-pattern '{
        "source": ["aws.cloudwatch"]
    }'

echo "Rule created."

echo "Connecting EventBridge rule to SQS..."

aws --endpoint-url=http://localhost:4566 \
    events put-targets \
    --rule cloudwatch-alarm-rule \
    --targets "Id"="incident-events","Arn"="arn:aws:sqs:us-west-1:000000000000:incident-events"

echo "Target connected."

echo "Done."