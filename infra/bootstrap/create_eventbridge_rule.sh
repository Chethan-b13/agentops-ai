#!/bin/bash

set -e

echo "Creating EventBridge rule..."

aws --endpoint-url=http://localhost:4566 \
    events put-rule \
    --name cloudwatch-alarm-rule \
    --event-pattern '{
        "source": ["aws.cloudwatch"]
    }'

echo "Rule created."