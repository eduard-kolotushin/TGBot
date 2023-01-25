import asyncio
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, nullable=False)
    history = Column(Text)
    update_time = Column(DateTime, nullable=False)

    def __init__(self, chat_id, history, update_time):
        self.chat_id = chat_id
        self.history = history
        self.update_time = update_time

    def __repr__(self):
        return "<History(chat_id='%s', history='%s', updated='%s')>" % (
            self.chat_id,
            self.history,
            self.update_time
        )


class Manager:
    local_history = dict()

    async def manage_history(self):
        for chat_id, history in self.local_history.items():
            h_to_del = list()
            for history_inst in history:
                if (datetime.datetime.now() - history_inst.update_time) > datetime.timedelta(hours=1):
                    h_to_del.append(history_inst)
            self.local_history[chat_id] = [v for v in self.local_history[chat_id] if v not in h_to_del]
        await asyncio.sleep(60)

    def add_history(self, history):
        chat_id = history.chat_id
        if chat_id in self.local_history:
            self.local_history[chat_id].append(history)
        else:
            self.local_history[chat_id] = [history]

    def extract_dialog(self, chat_id):
        text = None
        if chat_id not in self.local_history:
            return text
        history = self.local_history[chat_id]
        text = "\n".join([h.history for h in history])
        return text

    async def run(self):
        while 1:
            await self.manage_history()
