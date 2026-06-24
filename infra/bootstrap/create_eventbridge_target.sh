#!/bin/bash

set -e

echo "Connecting EventBridge rule to SQS..."

aws --endpoint-url=http://localhost:4566 \
    events put-targets \
    --rule cloudwatch-alarm-rule \
    --targets "Id"="incident-events","Arn"="arn:aws:sqs:us-west-1:000000000000:incident-events"

echo "Target connected."