import gpt_2_simple as gpt2
import random
import sys
import argparse
import requests

from app.constants import CHECKPOINT_DIR, RUN_NAME

"""
    CLS for FratGPT
"""

parser = argparse.ArgumentParser(
    description="Chat-bot trained on the conversations of the Gentlemen of Beta Sigma Psi National Lutheran Fraternity Eta Chapter"
    + "\u2122",
)

parser.add_argument(
    "--chat",
    help="chat with the bot",
    action="store_true",
    default=False,
)

parser.add_argument(
    "--long",
    help="let the bot do its thing",
    action="store_true",
    default=False,
)


def load():
    print(f"CHECKPOINT_DIR: {CHECKPOINT_DIR}")
    print(f"RUN_NAME      : {RUN_NAME}")
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=RUN_NAME, checkpoint_dir = CHECKPOINT_DIR)

    return sess


def response(sess=None, input_prefix: str = ""):
    if sess == None:
        raise Exception("No session provided :(")

    input_prefix: str = input_prefix

    sys.stdout.write(f"Computer:   *loading*\r")

    message: list = gpt2.generate(
        sess,
        return_as_list=True,
        run_name=RUN_NAME,
        prefix=input_prefix,
        length=(len(input_prefix) * 3),
        temperature=0.99,
        top_p=0.9,
    )[0].split("\n")

    try:
        sys.stdout.write(
            f"Computer:   {message[random.randint(1,len(message)-2)]}          \n"
        )
        sys.stdout.flush()
    except:
        sys.stdout.write(f"Computer:   {message[0]}          \n")
        sys.stdout.flush()


def convo(sess=None, input_prefix: str | None = None) -> None:

    if sess == None:
        raise Exception("No session provided :(")

    print(f" L{input_prefix}L ")

    if input_prefix:
        input_prefix: str = input_prefix
    else:
        input_prefix: str = str(input("You:        "))

    while input_prefix != "qq":
        sys.stdout.write(f"Computer:   *loading*\r")

        message: list = gpt2.generate(
            sess,
            return_as_list=True,
            run_name=RUN_NAME,
            prefix=input_prefix,
            length=(len(input_prefix) * 3),
            temperature=0.7,
            top_p=0.9,
        )[0].split("\n")

        try:
            sys.stdout.write(
                f"Computer:   {message[random.randint(1,len(message)-2)]}          \n"
            )
            sys.stdout.flush()
        except:
            sys.stdout.write(f"Computer:   {message[0]}          \n")
            sys.stdout.flush()

        input_prefix: str = str(input("You:        "))


def long(sess=None):

    if sess == None:
        raise Exception("No session provided :(")

    sys.stdout.write(f"*loading*\r")
    
    messages: list = gpt2.generate(
        sess,
        return_as_list=True,
        run_name=RUN_NAME,
        length=500,
        temperature=0.7,
        nsamples=10,
        batch_size=5,
    )

    sys.stdout.write(f"*loading*\r")
    [sys.stdout.write(message) for message in messages]
    sys.stdout.flush()


if getattr(parser.parse_args(), "chat"):
    sess = load()
    convo(sess=sess)

if getattr(parser.parse_args(), "long"):
    sess = load()
    long(sess=sess)