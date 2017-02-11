import argparse
import io
import os
from google.cloud import vision
from PIL import Image
from PIL import ImageDraw

'''
def detect_faces(path):
    """Detects faces in an image."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    faces = image.detect_faces()

    print('Faces:')
    for face in faces:

        print('anger: {}'.format(face.emotions.anger))
        print('joy: {}'.format(face.emotions.joy))
        print('surprise: {}'.format(face.emotions.surprise))
'''

# This method scans the image for faces and returns a list of image paths to all the faces it found
def scanImage(path):
    """Detects faces in an image."""
    vision_client = vision.Client()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision_client.image(content=content)

    faces = image.detect_faces()

    img = Image.open(path) #first we get the image to draw on
    draw = ImageDraw.Draw(img)
    faceNumber = 0
    #os.system('mkdir scans')
    #os.system('cd scans')
    for face in faces:
        vertices = face.bounds.vertices

        coords = []
        for vertice in vertices:
            c = (vertice.x_coordinate, vertice.y_coordinate) #we make a tuple coordinate object
            if (c[1] != None):
                coords.append(c) #and we add it to the array

        #now we have a polygon, so we draw
        if (len(coords) == 4): #if we did indeed get a rectangle
            draw.polygon(coords, outline=(255,255,255,255))
            name = "face_" + str(faceNumber)
            #crop(img, coords, name)
    img.save("scanned.jpg")
    faceNumber += 1

# Crops an image, assuming len(coords) == 4
def crop(img, coords, savename):
    print(coords)
    x = coords[0][0]
    y = coords[0][1]
    width = coords[2][0] - coords[0][0]
    height = coords[3][1] - coords[1][1]
    print("X: " + str(x))
    print("Y: " + str(y))
    print("HEIGHT: " + str(height))
    print("WIDTH: " + str(width))
    print("")
    img.crop((x, y, width, height))

    img.save(savename)


scanImage("george.JPG")