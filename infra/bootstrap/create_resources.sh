#!/bin/bash

set -e

echo "Creating SQS queue..."

aws --endpoint-url=http://localhost:4566 \
    sqs create-queue \
    --queue-name incident-events

echo "Done."