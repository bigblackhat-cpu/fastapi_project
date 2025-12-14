from fastapi import FastAPI,Depends
from celery_app import add

app = FastAPI()


async def mydepends():
    return {'hi':'there is mydepends'}

@app.get('/')
async def root():
    return {"message":"Hello there is fastapi app"}


@app.post('/api/ocr_transform')
async def ocr_transform():
    """
    Docstring for ocr_transform

    here will make a message to rabbitmq use celery, we will use delay 
    """
    print('celery test')
    resule = add.delay(name='He junie')
    
    return {'res': f'消息已发送，进入推理计算,{resule.ready()}'}



