from fastapi import APIRouter


test_router = APIRouter(prefix='/test', tags=['Test'])


@test_router.get('/')
async def get_test(number: int):
    return {
        'Number': number * 2
    }