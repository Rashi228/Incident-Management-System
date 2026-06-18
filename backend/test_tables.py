import asyncio
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_tables():
    from app.db.session import engine
    from sqlalchemy import text
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print("Tables in public schema:")
        for t in tables:
            print(f"- {t}")

if __name__ == "__main__":
    asyncio.run(test_tables())
