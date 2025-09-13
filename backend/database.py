import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://Harsh:1q2w3e4r@cluster0.6xpkx5x.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db = client["emailgen"]   # Database
emails_collection = db["emails"]   # Collection
