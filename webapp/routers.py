from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def root():
    return {"message":"Hello there is fastapi app"}

@router.get('/ping')
async def pint():
    return {'status':'ok'}

from .basemodel_type import OcrImageSerializer
@router.post('/api/ocr_mock')
async def ocr_transform_mock(imageSerializer: OcrImageSerializer):
    print('process image start ...')
    print(imageSerializer.image_url)
    print('process image end ...')
    return {'taskid':12333713}


from .celery_app.tasks import pingTask
@router.post('/api/pingTask')
async def pingTask(pic_url:str):
    """
    Docstring for ocr_transform

    here will make a message to rabbitmq use celery, we will use delay 
    """

    result = pingTask.delay()
    
    return {'res': f'消息已发送，进入推理计算,{result.ready()}'}



