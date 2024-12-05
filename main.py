import asyncio
from fastapi import FastAPI
from jsonplaceholder_requests import fetch_users_data, fetch_posts_data
from models import init_db, engine, User, Post
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

app = FastAPI()

async def add_users_to_db(users_data, session):
    for user in users_data:
        new_user = User(name=user['name'], username=user['username'], email=user['email'])
        session.add(new_user)
    await session.commit()

async def add_posts_to_db(posts_data, session):
    for post in posts_data:
        new_post = Post(user_id=post['userId'], title=post['title'], body=post['body'])
        session.add(new_post)
    await session.commit()

@app.on_event("startup")
async def startup():
    await init_db()

@app.get("/load_data")
async def load_data():
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        users_data, posts_data = await asyncio.gather(
            fetch_users_data(),
            fetch_posts_data(),
        )

        await add_users_to_db(users_data, session)
        await add_posts_to_db(posts_data, session)

    return {"message": "Data loaded successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
