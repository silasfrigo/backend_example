from fastapi import APIRouter, Response
router = APIRouter()


@router.get('/simple')
async def hello_world(response: Response):
    return {
        "hello": "world"
    }


@router.post('/prescriptions')
async def create_prescription(response: Response):
    return {
        "foo": "bar"
    }
