import asyncio
from typing import Optional

from googleapiclient.discovery import build

from app.core.config import settings

class VideoService:
    def __init__(self):
        self.youtube = None
        if settings.YOUTUBE_API_KEY:
            self.youtube = build(
                "youtube",
                "v3",
                developerKey=settings.YOUTUBE_API_KEY,
                cache_discovery=False,
            )

    async def find_lesson_video(self, search_term: str) -> Optional[dict]:
        """Search a relevant video using YouTube Data API v3."""
        if not self.youtube:
            print("YOUTUBE_API_KEY missing; skipping YouTube lookup.")
            return None

        try:
            def run_search():
                request = self.youtube.search().list(
                    q=search_term,
                    part="snippet",
                    type="video",
                    maxResults=1,
                    safeSearch="moderate",
                    videoEmbeddable="true",
                )
                return request.execute()

            response = await asyncio.to_thread(run_search)
            items = response.get("items", [])
            if items:
                item = items[0]
                snippet = item.get("snippet", {})
                video_id = item.get("id", {}).get("videoId")
                if not video_id:
                    return None
                return {
                    "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                    "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url")
                    or snippet.get("thumbnails", {}).get("default", {}).get("url"),
                    "duration": None,
                    "view_count": None,
                    "id": video_id,
                    "title": snippet.get("title"),
                }
        except Exception as e:
            print(f"YouTube search failed for '{search_term}': {e}")

        return None

video_service = VideoService()
