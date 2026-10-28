from fastapi import APIRouter, Depends, HTTPException
from app.services.ai_service import ai_service
from app.services.video_service import video_service
from app.core.auth import get_current_user
from pydantic import BaseModel
import asyncio
import uuid

router = APIRouter(prefix="/ai", tags=["AI Course Architect"])

class GenerateRequest(BaseModel):
    topic: str
    difficulty: str = "Beginner"

class ChatRequest(BaseModel):
    message: str
    conversation_history: list = []

@router.post("/generate")
async def generate_course(request: GenerateRequest, current_user=Depends(get_current_user)):
    """
    Magic Endpoint: Generates a full course from a prompt.
    1. Generates Syllabus via Gemini
    2. Enriches lessons with YouTube videos
    """
    try:
        # 1. Generate Syllabus
        syllabus = await ai_service.generate_syllabus(request.topic, request.difficulty)
        
        # 2. Enrich with Videos (in parallel for speed)
        for m_idx, module in enumerate(syllabus.get("modules", [])):
            module["id"] = f"m-{uuid.uuid4().hex[:6]}"
            module["order"] = m_idx
            
            # Prepare search tasks for all lessons in this module
            tasks = []
            for lesson in module.get("lessons", []):
                tasks.append(video_service.find_lesson_video(lesson["search_term"]))
            
            # Run searches
            video_results = await asyncio.gather(*tasks)
            
            # Assign results
            for l_idx, (lesson, video_res) in enumerate(zip(module["lessons"], video_results)):
                lesson["id"] = f"l-{uuid.uuid4().hex[:6]}"
                lesson["order"] = l_idx
                if video_res:
                    lesson["youtube_url"] = video_res["youtube_url"]
                    lesson["thumbnail"] = video_res["thumbnail"]
                    lesson["content"] = f"High-quality instructional content for {lesson['title']}."
                else:
                    lesson["youtube_url"] = ""
                    lesson["content"] = "No video found. Please search manually."

        # 3. Finalize Course Object
        user_id = str(current_user.get("id", current_user.get("_id", "1")))
        syllabus["instructor_id"] = user_id
        syllabus["difficulty"] = request.difficulty
        syllabus["status"] = "draft"
        
        return syllabus

    except Exception as e:
        print(f"Course generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_ai(request: ChatRequest, current_user=Depends(get_current_user)):
    """
    Chat with AI Learning Assistant using Groq
    """
    try:
        from groq import Groq
        from app.core.config import settings
        
        if not settings.GROQ_API_KEY:
            raise HTTPException(status_code=500, detail="Groq API key not configured")
        
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # Build conversation messages
        messages = [
            {
                "role": "system",
                "content": """You are a helpful AI Learning Assistant for an online Learning Management System (LMS). 
Your role is to help students with:
- Course recommendations and guidance
- Learning strategies and study tips
- Platform navigation and features
- Answering questions about topics they're learning
- Motivation and encouragement

Be friendly, concise, and educational. Use emojis occasionally to make responses engaging.
If asked about specific course content, provide helpful explanations.
Always encourage continuous learning and growth."""
            }
        ]
        
        # Add conversation history if provided
        for msg in request.conversation_history[-5:]:  # Last 5 messages for context
            messages.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": request.message
        })
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            stream=False
        )
        
        response_text = chat_completion.choices[0].message.content
        
        return {
            "response": response_text,
            "model": "llama-3.1-8b-instant",
            "tokens_used": chat_completion.usage.total_tokens if hasattr(chat_completion, 'usage') else 0
        }
        
    except Exception as e:
        print(f"Chat error: {str(e)}")
        # Fallback response if Groq fails
        return {
            "response": "I'm having trouble connecting to my AI brain right now. Please try again in a moment! 🤖",
            "error": str(e)
        }
