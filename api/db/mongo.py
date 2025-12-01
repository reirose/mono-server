from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from api.config import settings


class DB:
    def __init__(self, mongo_uri):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db: AsyncIOMotorDatabase | None = None

    def connect(self):
        self.db = self.client.get_database("mono")
        return self


class UserDB(DB):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collection: AsyncIOMotorCollection | None = None

    def connect(self):
        self.collection = self.db.get_collection("users")
        return self


class CardsDB(DB):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.collection: AsyncIOMotorCollection | None = None

    def connect(self):
        self.collection = self.db.get_collection("cards")
        return self


db = DB(settings.mongo_uri)
db.connect()
