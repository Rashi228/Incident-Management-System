import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_create_article():
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.models.article import Article
    from sqlalchemy.future import select

    async with SessionLocal() as s:
        res = await s.execute(select(User))
        users = res.scalars().all()
        print(f"Total users in DB: {len(users)}")
        for u in users:
            print(f"- {u.email} ({u.role})")
        
        if not users:
            return
        
        u = users[0]
            
        print(f"Testing with user: {u.id}")
        
        try:
            db_obj = Article(
                title="Test Article from script",
                content="This is a test article content that is long enough to pass validation.",
                category="Software",
                author_id=u.id
            )
            s.add(db_obj)
            await s.commit()
            await s.refresh(db_obj)
            print(f"SUCCESS! Article created with id: {db_obj.id}")
        except Exception as e:
            print(f"FAILED TO CREATE ARTICLE: {type(e)}")
            print(e)

if __name__ == "__main__":
    asyncio.run(test_create_article())
