import os


class Config:
    TGTOKEN = os.getenv('TGTOKEN', default="Fuck you I don't know your fucking token!")
