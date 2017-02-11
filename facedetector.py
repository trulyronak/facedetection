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
    os.system('echo wiping old scans')
    os.system('rm -rf scans')
    os.system('rm scanned.jpg')
    os.system('mkdir scans')
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
            name = "face_" + str(faceNumber) + ".jpg"
            crop(img, coords, name)
        faceNumber += 1
    img.save("totalscan.jpg")
    os.system('mv totalscan.jpg scans/')
# Crops an image, assuming len(coords) == 4
def crop(img, coords, savename):
    #print(coords)
    #print("IMAGE SIZE: " + str(img.size))
    x1 = coords[0][0]
    y1 = coords[0][1]
    x2 = coords[2][0]
    y2 = coords[2][1]

    #width = (x2 - x1)
    #height = (y2 - y1)
    #print("X: " + str(x1))
    #print("Y: " + str(y1))
    #print("HEIGHT: " + str(height))
    #print("WIDTH: " + str(width))
    #print("")
    newImg = img.crop((x1, y1, x2, y2))
    
    newImg.save(savename)
    cmd = "mv " + savename + " scans/"
    os.system(cmd) 

scanImage("brilliant.jpg")