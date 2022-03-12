from pyrogram import Client
from pyromod import listen
from config import ApiID, ApiHash, Token
import logging

logging.basicConfig(level=logging.INFO)

app = Client(
    ':memory:',
    api_id=ApiID,
    api_hash=ApiHash,
    bot_token=Token,
    plugins=dict(root='plugs'),
)

app.run()
