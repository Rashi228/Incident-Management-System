import asyncio
import json
import uuid
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_db():
    from app.db.session import async_session
    from sqlalchemy.future import select
    from app.models.article import Article
    
    async with async_session() as session:
        result = await session.execute(select(Article))
        articles = result.scalars().all()
        print(f"Found {len(articles)} articles.")

asyncio.run(test_db())
