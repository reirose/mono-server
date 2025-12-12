from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from api.config import settings
from api.models.user import User


class DB:
    def __init__(self, mongo_uri):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db: AsyncIOMotorDatabase | None = None

    def connect(self):
        self.db = self.client.get_database("mono")
        return self


class UserDB:
    def __init__(self, mongo_uri):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db: AsyncIOMotorDatabase | None = None
        self.collection: AsyncIOMotorCollection | None = None

    def connect(self, master_db):
        self.collection = master_db.db.get_collection("users")
        return self

    async def get_user(self, telegram_id: int) -> User:
        db_data: dict = await self.collection.find_one({"telegram_id": telegram_id})
        if not db_data:
            return User(telegram_id=None, username=None, collection={})
        return User(**db_data)

    async def write_user(self, user: User) -> bool:
        user_data: dict = user.model_dump()
        akn: bool = (await self.collection.update_one({"telegram_id": user.telegram_id}, {"$set": user_data})).acknowledged
        return akn


class CardsDB:
    def __init__(self, mongo_uri):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db: AsyncIOMotorDatabase | None = None
        self.collection: AsyncIOMotorCollection | None = None

    def connect(self, master_db):
        self.collection = master_db.db.get_collection("cards")
        return self


db = DB(settings.mongo_uri)
user_db = UserDB(settings.mongo_uri)
cards_db = CardsDB(settings.mongo_uri)
db.connect()
user_db.connect(db)
cards_db.connect(db)
