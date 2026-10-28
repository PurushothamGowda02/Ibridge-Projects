import asyncio
from app.services.video_service import video_service
import sys

# Ensure backend directory is in path
sys.path.insert(0, '.')

async def test_youtube():
    print("Testing YouTube video search...")
    result = await video_service.find_lesson_video("Python Programming Tutorial for Beginners")
    if result:
        print(f"SUCCESS: Found video: {result['title']}")
        print(f"URL: {result['youtube_url']}")
    else:
        print("FAILURE: No video found.")

if __name__ == "__main__":
    asyncio.run(test_youtube())
