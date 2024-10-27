import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"  # Replace with your MongoDB connection string

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
database = client.school_blog

blog_collection = database.get_collection("blogs")
