#!/usr/bin/python

import cv2
import numpy as np
import face_recognition


def image_from_bytes(im_bytes):
    arr = np.fromstring(im_bytes, np.uint8)
    return cv2.imdecode(arr, 1)


def image_to_bytes(image):
    im_bytes = cv2.imencode('.jpg', image)[1].tostring()
    return im_bytes

def detect_face(image):
    img_rect = image.copy()
    face_crop = None
    status = 'failed'
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) > 0:
        # Print the location of each face in this image
        top, right, bottom, left = face_locations[0]
        print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    
        # You can access the actual face itself like this:
        face_crop = image[top:bottom, left:right]
        # Blue color in BGR 
        color = (0, 255, 0) 
        
        # Line thickness of 2 px 
        thickness = 40
  
        # Using cv2.rectangle() method 
        # Draw a rectangle with blue line borders of thickness of 2 px 
        face_roi = cv2.rectangle(img_rect, (left,top), (right,bottom), color, thickness) 
        status = 'success'
        
    return face_crop, face_roi, status










