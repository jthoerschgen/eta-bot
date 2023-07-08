import asyncio
from clip_interrogator import Interrogator
import gpt_2_simple as gpt2
import io
import logging
from PIL import Image
import random
import requests
import sys
import tensorflow as tf

from constants import CHECKPOINT_DIR, RUN_NAME

logger = logging.getLogger(__name__)


def load_sess(sess: tf.compat.v1.Session = None) -> tf.compat.v1.Session:
    """Loads a gpt2 session to use for generating messages

    Args:
        sess (tf.compat.v1.Session, optional): Previous gpt2 session. Defaults to None.

    Returns:
        tf.compat.v1.Session: Session used for generating messages
    """
    if sess:
        return_sess: tf.compat.v1.Session = gpt2.reset_session(sess)
    else:
        return_sess: tf.compat.v1.Session = gpt2.start_tf_sess()

    gpt2.load_gpt2(sess=return_sess, checkpoint_dir=CHECKPOINT_DIR, run_name=RUN_NAME)
    return return_sess


async def generate_response(
    sess: tf.compat.v1.Session,
    input: str = "",
    keep_whole: bool = False,
    length: int = random.randint(30, 80),
    temperature: float = random.randint(45, 75) / 100,
) -> str:
    """Generates a message from chat bot model.

    Args:
        sess (tf.compat.v1.Session): gpt2 session
        input (str, optional): String used as prefix for response. Defaults to "".
        keep_whole (bool, optional): If True, return entire response. Defaults to False.
        length (int, optional): Length of output. Defaults to value between 30 and 80.
        temperature (float, optional):
            How crazy response is, must be between 0-1.
            Defaults to to value between 0.6 and 0.9.

    Returns:
        str: generated message
    """
    assert (
        temperature >= 0 and temperature <= 1
    ), f"Provided temperature={temperature}, must be between 0-1"

    async with asyncio.Lock():
        logger.info("Generating message using:")
        logger.info(f"  input: {input}" if len(input) > 0 else "  input: None")
        logger.info(f"  length: {length}")
        logger.info(f"  temperature: {temperature}")

        sys.stdout.write("*generating message*\r")
        message: list[str] = gpt2.generate(
            sess,
            return_as_list=True,
            run_name=RUN_NAME,
            prefix=input,
            length=length,
            temperature=temperature,
        )[0].split("\n")
        sys.stdout.flush()

        if keep_whole:
            return "\n".join(message)
        else:
            try:
                return message[random.randint(1, len(message) - 1)]
            except Exception(IndexError):
                return message[0]


async def describe_image(sess: Interrogator, url: str) -> str:
    """Returns description of an image from image URL

    Args:
        sess (Interrogator): Clip Interrogator object
        url (str): URL of image to be described

    Returns:
        str: Generated description of photo
    """
    with io.BytesIO(
        requests.get(url).content
    ) as img_buf:  # download image from message
        img: Image.Image = Image.open(img_buf).convert("RGB")
        return (
            sess.interrogate_fast(img)
            .split(",")[0]
            .replace("araffe", "")
            .replace("arafed", "")
        )
