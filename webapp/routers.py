from fastapi import APIRouter
from celery.result import AsyncResult
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

from .basemodel_type import OcrImageSerializer
from .celery_app.tasks import ocr_api
@router.post('/api/ocr_server')
async def ocr_transform_mock(imageSerializer: OcrImageSerializer):
    print('process image start ...')
    # print(imageSerializer.image_url)
    res: AsyncResult = ocr_api.delay(imageSerializer.image_url)
    print('process image end ...')
    
    return {'taskid':res.id}

from .celery_app.tasks import pingTask
@router.post('/api/pingTask')
async def pingTaskApi():
    """
    Docstring for ocr_transform

    here will make a message to rabbitmq use celery, we will use delay 
    """

    result = pingTask.delay()
    
    return {'res': f'消息已发送，进入推理计算,{result.ready()}'}


from .celery_app.tasks import tes_single
@router.post('/api/tes_single')
async def tesModelApi():
    result = tes_single.delay()

    return {'res':f'消息已发送，进入推理计算,{result.ready()}'}



