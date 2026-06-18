import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def generate_token():
    from app.core.security import create_access_token
    from app.db.session import SessionLocal
    from app.models.user import User
    from sqlalchemy.future import select

    async with SessionLocal() as s:
        res = await s.execute(select(User).limit(1))
        u = res.scalars().first()
        if u:
            token = create_access_token(str(u.id), {'role': u.role})
            print(f"export TOKEN={token}")
        else:
            print("No users found")

if __name__ == "__main__":
    asyncio.run(generate_token())
