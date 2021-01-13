#!/usr/bin/python

import logging

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from utils.utils import image_from_bytes, detect_face

import uvicorn
import cv2
import datetime

# Global
app    = Starlette()
logger = logging.getLogger(__name__)


# Endpoints


@app.route('/image_saver', methods=['POST'])
async def endpoint_extrac(request):
    image = None
    
    try:
        #Leer los bytes de la imagen enviada como multipart
        data = await request.form()
        print(data)
        byte_array = await data['image'].read()
    
        # Crear imagen desde bytes
        image = image_from_bytes(byte_array)
    
        # Detect faces into image
        face_crop, face_roi, status = detect_face(image)
    
        # Get the current date
        now = datetime.datetime.now()
        day_month_year = '{}-{}-{}'.format(now.year, now.month, now.day)
        time = '{}-{}-{}'.format(now.hour, now.minute, now.second)
    
        # Make the name for the file and write the file
        file_name = 'debug_faces/img-' + day_month_year + '-' + time + '.png'
        file_name_face = 'debug_faces/img-' + day_month_year + '-' + time + '_face.png'
        file_name_detect = 'debug_faces/img-' + day_month_year + '-' + time + '_detect.png'
        
        # Make the name for the file and write the file 
        cv2.imwrite(file_name, image)

        if status == 'success':
            cv2.imwrite(file_name_face, face_crop)
            cv2.imwrite(file_name_detect, face_roi)
        
    except:
        raise HTTPException(400)
        
    # Response
    return JSONResponse({'status':'Imagen almacenada exitosamente'})




@app.exception_handler(400)
async def missing_parameter(request, exc):
    """No se encontró algún parámetro obligatorio en la petición
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': 'Bad Request'}
    )


@app.exception_handler(404)
async def not_found(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': 'Not Found'}
    )


@app.exception_handler(422)
async def unprocessable(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': 'Unprocessable Entity'}
    )


# Setup y launcher


def setup_app():
    global app
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_headers=['X-Requested-With', 'Content-Type']
    )


def run_app():
    uvicorn.run(app=app, host='0.0.0.0', port=5041)


def main():
    setup_app()
    run_app()


if __name__ == '__main__':
    main()
