from pydantic import BaseModel

CHECKPOINT_DIR = "/home/jimmy/GitHub/etaBot/checkpoint/"
RUN_NAME = "run5"


class GroupMeMessage(BaseModel):
    attachments: list
    avatar_url: str
    created_at: int
    group_id: str
    id: str
    name: str
    sender_id: str
    sender_type: str
    source_guid: str
    system: bool
    text: str
    user_id: str
