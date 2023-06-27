from clip_interrogator import Config, Interrogator
from colorama import Fore, Back, Style
from fastapi import FastAPI
import gpt_2_simple as gpt2
import logging
import os
import uvicorn

from constants import GroupMeMessage
from functions.funcs import *
from functions.chatbot_funcs import *
from __init__ import args

logger = logging.getLogger(__name__)


app = FastAPI()


@app.on_event("startup")
async def startup():
    print(Fore.GREEN)
    print("    ______           __  __________  ______")
    print("   / ____/________ _/ /_/ ____/ __ \/_  __/")
    print("  / /_  / ___/ __ `/ __/ / __/ /_/ / / /   ")
    print(" / __/ / /  / /_/ / /_/ /_/ / ____/ / /    ")
    print("/_/   /_/   \__,_/\__/\____/_/     /_/     ")
    print(Style.RESET_ALL)
    print("Where fraternity and event technology meet")
    print()

    if args.testing:
        logger.info("Testing Mode:" + Fore.RED + " ON" + Style.RESET_ALL)

    logger.info("Loading GPT Session...")
    app.gpt_sess = load_sess()  ## Load GPT-2 Simple FratGPT model

    logger.info("Loading Clip Interrogator Session...")
    app.ci: Interrogator = Interrogator(Config(device="cpu"))


@app.post("/bot/message")
async def recieve(message: GroupMeMessage):
    if message.name != os.environ["BOT_NAME"]:  ## prevents schizophrenia
        if message.text.upper().startswith(
            "@" + os.environ["BOT_NAME"].upper() + " STORYTIME"
        ):
            await post_message(
                await generate_response(
                    sess=app.gpt_sess,
                    input=message.text[
                        len("@" + os.environ["BOT_NAME"] + " STORYTIME") :
                    ],
                    keep_whole=True,
                    length=250,
                    temperature=0.9,
                )
            )

        elif message.text.upper().startswith("@" + os.environ["BOT_NAME"].upper()):
            if not message.attachments:
                await post_message(
                    await generate_response(
                        sess=app.gpt_sess,
                        input=message.text[len("@" + os.environ["BOT_NAME"]) :],
                    )
                )
            else:
                for attachment in message.attachments:
                    if attachment["type"] == "image":
                        image_description: str = await describe_image(
                            sess=app.ci, url=attachment["url"]
                        )
                        if message.text.upper().startswith(
                            "@" + os.environ["BOT_NAME"].upper() + " IDENTIFY"
                        ):
                            await post_message(image_description)
                        else:
                            await post_message(
                                await generate_response(
                                    sess=app.gpt_sess,
                                    input=message.text[
                                        len("@" + os.environ["BOT_NAME"]) :
                                    ]
                                    + " "
                                    + image_description,
                                )
                            )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=25566,
        log_level="info",
        reload=True,
    )
