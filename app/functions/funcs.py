import json
import logging
import os
import random
import requests

logger = logging.getLogger(__name__)


async def post_message(message: str) -> bool:
    """Sends a string of text to the group the bot is in.

    Args:
        message (str): The text being sent

    Returns:
        bool: If the post was successful
    """
    response: requests.Response = requests.post(
        url="https://api.groupme.com/v3/bots/post",
        headers=(
            {
                "Content-Type": "application/x-www-form-urlencoded",
            }
        ),
        data=json.dumps(
            {
                "text": message,
                "bot_id": os.environ["BOT_ID"],
            }
        ),
    )
    return response.ok


def get_image_url(image: bytes) -> str:
    """Sends an image as bytes and gets a URL usable for GroupMe

    Args:
        image (bytes): Image bytes

    Returns:
        str: URL of image usable for GroupMe
    """
    return json.loads(
        requests.post(
            url="https://image.groupme.com/pictures",
            data=image,
            headers={
                "Content-Type": "image/jpeg",
                "X-Access-Token": os.environ["GROUP_ME_TOKEN"],
            },
        ).content.decode()
    )["payload"]["url"]


async def post_image(image: bytes) -> bool:
    response = requests.post(
        "https://api.groupme.com/v3/bots/post",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data=json.dumps(
            {
                "attachments": [
                    {
                        "type": "image",
                        "url": get_image_url(image),
                    },
                ],
                "bot_id": os.environ["BOT_ID"],
            }
        ),
    )
    return response.ok
