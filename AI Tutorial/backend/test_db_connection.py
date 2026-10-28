"""
Quick script to test MongoDB connection
Run this to verify MongoDB is accessible before testing registration
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

async def test_connection():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/ai_tutorial")
    print(f"Testing connection to: {mongo_uri}")
    print("-" * 60)
    
    try:
        # Try to connect
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        await client.admin.command('ping')
        print("✅ SUCCESS: MongoDB is accessible!")
        
        # Get database
        db = client.ai_tutorial
        
        # Check collections
        collections = await db.list_collection_names()
        print(f"\n📦 Available collections: {collections}")
        
        # Check users count
        users_count = await db.users.count_documents({})
        print(f"👥 Total users in database: {users_count}")
        
        if users_count > 0:
            # Show sample user (without password)
            sample_user = await db.users.find_one({}, {"password_hash": 0})
            print(f"\n📄 Sample user:")
            print(f"   Email: {sample_user.get('email')}")
            print(f"   Name: {sample_user.get('full_name')}")
            print(f"   Role: {sample_user.get('role')}")
        
        client.close()
        print("\n✅ Database connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Cannot connect to MongoDB")
        print(f"   Error details: {str(e)}")
        print("\n💡 Solutions:")
        print("   1. Make sure Docker Desktop is running")
        print("   2. Run: docker run -d --name lms_db -p 27017:27017 mongo:latest")
        print("   3. Or use MongoDB Atlas (cloud) - see MONGODB_SETUP_INSTRUCTIONS.md")
        return False

if __name__ == "__main__":
    print("🔍 MongoDB Connection Test")
    print("=" * 60)
    asyncio.run(test_connection())
