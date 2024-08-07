from typing import List, Optional
from fastapi import Depends, FastAPI, Form, status
from prisma import Prisma, models, partials
from pydantic import EmailStr

app = FastAPI()

async def get_prisma_client():
    prisma = Prisma()
    try:
        await prisma.connect()
        yield prisma
    except Exception as e:
        raise e
    finally:
        await prisma.disconnect()


@app.post("/users", status_code=status.HTTP_201_CREATED)
async def create_user(
    email: EmailStr = Form(),
    name: Optional[str] = Form(None),
    prisma: Prisma = Depends(get_prisma_client)
):
    return await prisma.user.create(data={"email": email, "name": name})

@app.get("/users", response_model=List[partials.UserSchema])
async def get_users(prisma: Prisma = Depends(get_prisma_client)):
    return await partials.UserSchema.prisma(prisma).find_many()

@app.patch("/users/{id}", response_model=models.User)
async def update_user(
    id: int,
    name: Optional[str] = Form(None),
    prisma: Prisma = Depends(get_prisma_client)
):
    return await prisma.user.update(where={"id": id}, data={"name": name})

@app.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: int,
    prisma: Prisma = Depends(get_prisma_client)
):
    return await prisma.user.delete(where={"id": id})
