from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = "mongodb://db-nutrition:27017/nutrition_db"

client = AsyncIOMotorClient(MONGO_URL)
database = client.get_database("nutrition_db")

def get_nutrition_db():
    return database.get_collection("historico_dietas")