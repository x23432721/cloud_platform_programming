import boto3
import json
from django.conf import settings
from botocore.exceptions import ClientError

import logging

logger = logging.getLogger(__name__)

s3_client = boto3.client("s3", region_name=settings.AWS_REGION)
sqs_client = boto3.client("sqs", region_name=settings.AWS_REGION)


def upload_file_to_s3(file_obj, key_prefix: str) -> str:

    bucket = settings.AWS_S3_BUCKET
    key = f"{key_prefix}/{file_obj.name}"

    try:
        s3_client.upload_fileobj(
            file_obj,
            bucket,
            key,
            ExtraArgs={"ACL": "private", "ContentType": file_obj.content_type}
        )
    except ClientError as e:
        print("Error uploading to S3:", e)
        return ""

    return f"https://{bucket}.s3.{settings.AWS_REGION}.amazonaws.com/{key}"

def send_booking_to_sqs(booking) -> str | None:

    payload = {
        "booking_id": booking.id,
        "user_id": booking.user.id,
        "username": booking.user.username,
        "user_email": booking.user.email,
        "vehicle": str(booking.vehicle),
        "service_name": booking.service.name,
        "service_code": booking.service.code,
        "preferred_date": booking.preferred_date.isoformat() if booking.preferred_date else None,
        "created_at": booking.created_at.isoformat() if booking.created_at else None,
        "estimated_price": str(booking.estimated_price),
        "estimated_completion_time": booking.estimated_completion_time.isoformat()
        if booking.estimated_completion_time
        else None,
    }

    try:
        response = sqs_client.send_message(
            QueueUrl=settings.AWS_SQS_QUEUE_URL,
            MessageBody=json.dumps(payload),
        )
        message_id = response.get("MessageId")
        logger.info("Sent booking to SQS. MessageId=%s", message_id)
        print("DEBUG SQS MessageId:", message_id)
        return message_id
    except ClientError as e:
        logger.exception("Error sending booking message to SQS")
        print("Error sending booking message to SQS:", e)
        return None
