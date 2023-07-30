import csv
import logging
import os
import random
from datetime import datetime
from urllib.request import urlopen

import uvicorn
from __init__ import args
from clip_interrogator import Config, Interrogator
from colorama import Fore, Style
from constants import GroupMeMessage
from fastapi import FastAPI
from functions.chatbot_funcs import (describe_image, generate_response,
                                     load_sess)
from functions.funcs import (is_mentioned, post_image, post_message,
                             trim_mention)

logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")
async def startup():
    print(Fore.GREEN)
    print("    ______           __  __________  ______")
    print("   / ____/________ _/ /_/ ____/ __ \\/_  __/")
    print("  / /_  / ___/ __ `/ __/ / __/ /_/ / / /   ")
    print(" / __/ / /  / /_/ / /_/ /_/ / ____/ / /    ")
    print("/_/   /_/   \\__,_/\\__/\\____/_/     /_/     ")
    print(Style.RESET_ALL)
    print("Where fraternity and event technology meet")
    print()

    if args.testing:
        logger.info("Testing Mode:" + Fore.RED + " ON" + Style.RESET_ALL)

    logger.info("Loading GPT Session...")
    app.gpt_sess = load_sess()  # Load GPT-2 Simple FratGPT model

    logger.info("Loading Clip Interrogator Session...")
    app.ci: Interrogator = Interrogator(Config(device="cpu"))


@app.post("/bot/message")
async def recieve(message: GroupMeMessage):
    logger.info(f"SENDER:     {message.name}, {message.sender_id}")
    logger.info(f"TIME STAMP: {datetime.utcfromtimestamp(message.created_at)}")
    logger.info(f"MESSAGE:    {message.text}")

    logger.info("ATTACHMENTS")
    for attachment in message.attachments:
        logger.info(attachment)

    if message.name != os.environ["BOT_NAME"]:  # prevents schizophrenia

        if is_mentioned(message=message.text, keyword="monkey"):
            await post_image(urlopen(message.avatar_url).read())  # DOXXED!

        elif is_mentioned(message=message.text, keyword="image"):
            with open(os.environ["IMAGE_URL_CSV"], "r") as csv_file:
                img_url: str = random.choice(list(csv.reader(csv_file)))[0]
                logger.info(img_url)
            await post_image(urlopen(img_url).read())
        
        elif is_mentioned(message=message.text, keyword="storytime"):
            await post_message(
                await generate_response(
                    sess=app.gpt_sess,
                    input=trim_mention(message=message.text, keyword="storytime"),
                    keep_whole=True,
                    length=250,
                    temperature=0.9,
                )
            )
        elif is_mentioned(message=message.text):
            if not message.attachments:
                await post_message(
                    await generate_response(
                        sess=app.gpt_sess,
                        input=trim_mention(message=message.text),
                    )
                )
            else:
                for attachment in message.attachments:
                    if attachment["type"] == "image":
                        image_description: str = await describe_image(
                            sess=app.ci, url=attachment["url"]
                        )
                        if is_mentioned(message=message.text, keyword="identify"):
                            await post_message(image_description)
                        else:
                            await post_message(
                                await generate_response(
                                    sess=app.gpt_sess,
                                    input=image_description
                                    + ". "
                                    + trim_mention(message=message.text),
                                )
                            )
        else:
            roll: int = random.randint(1, 100)
            logger.info(f"ROLLED: {roll}")
            if roll <= 10:
                logger.info("Success!")
                await post_message(
                    await generate_response(
                        sess=app.gpt_sess,
                        input=message.text,
                    )
                )
            else:
                logger.info("Failure!")

    return True


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=25566,
        log_level="info",
        reload=True,
    )
