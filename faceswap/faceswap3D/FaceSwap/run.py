# run command: python run.py <full GIF path with filename+extention> <full face-image path with filename+extention> <output file's name+extention>
import os
import time
import dlib
import cv2
import numpy as np
import subprocess
from OpenGL.GL import *
from OpenGL.GLU import *
import sys


import models
import NonLinearLeastSquares
import ImageProcessing

from drawing import *

import FaceRendering
import utils


start_time = time.time()
print("Press T to draw the keypoints and the 3D model")
print("Press R to start recording to a video file")
output_filename = sys.argv[3]
repo_root_dir = ".."
replace_face = sys.argv[2]
initial_video = sys.argv[1]
slow_down_by = 2

#you need to download shape_predictor_68_face_landmarks.dat from the link below and unpack it where the solution file is
#http://sourceforge.net/projects/dclib/files/dlib/v18.10/shape_predictor_68_face_landmarks.dat.bz2

#loading the keypoint detection model, the image and the 3D model
predictor_path = os.path.join(os.path.dirname(__file__), repo_root_dir, "shape_predictor_68_face_landmarks.dat")
image_name = replace_face #os.path.join(os.path.dirname(__file__), repo_root_dir, "data", replace_face)
initial_video_path = initial_video #os.path.join(os.path.dirname(__file__), repo_root_dir, "data", initial_video)
#the smaller this value gets the faster the detection will work
#if it is too small, the user's face might not be detected
maxImageSizeForDetection = 320

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
mean3DShape, blendshapes, mesh, idxs3D, idxs2D = utils.load3DFaceModel( os.path.join(os.path.dirname(__file__), "..", "candide.npz"))

projectionModel = models.OrthographicProjectionBlendshapes(blendshapes.shape[0])

modelParams = None
lockedTranslation = False
drawOverlay = False
cap = cv2.VideoCapture(initial_video_path)
fps = 30
ret, cameraImg = cap.read()
if ret==False:
    exit(0)

textureImg = cv2.imread(image_name)
textureCoords = utils.getFaceTextureCoords(textureImg, mean3DShape, blendshapes, idxs2D, idxs3D, detector, predictor)
renderer = FaceRendering.FaceRenderer(cameraImg, textureImg, textureCoords, mesh)


print("Starting video writer")
writer = cv2.VideoWriter(os.path.join(os.path.dirname(__file__),
                                        repo_root_dir,
                                        output_filename),
                                        cv2.VideoWriter_fourcc(*'DIVX'),
                                        fps,
                                        (cameraImg.shape[1], cameraImg.shape[0]))
if writer.isOpened():
    print("Writer succesfully opened")
else:
    print("Writer opening failed")
    exit(0)

while True:
    ret, cameraImg = cap.read()
    if ret==True:
        
        shapes2D = utils.getFaceKeypoints(cameraImg, detector, predictor, maxImageSizeForDetection)

        if shapes2D is not None:
            for shape2D in shapes2D:
                #3D model parameter initialization
                modelParams = projectionModel.getInitialParameters(mean3DShape[:, idxs3D], shape2D[:, idxs2D])

                #3D model parameter optimization
                modelParams = NonLinearLeastSquares.GaussNewton(modelParams, projectionModel.residual, projectionModel.jacobian, ([mean3DShape[:, idxs3D], blendshapes[:, :, idxs3D]], shape2D[:, idxs2D]), verbose=0)

                #rendering the model to an image
                shape3D = utils.getShape3D(mean3DShape, blendshapes, modelParams)
                renderedImg = renderer.render(shape3D)

                #blending of the rendered face with the image
                mask = np.copy(renderedImg[:, :, 0])
                renderedImg = ImageProcessing.colorTransfer(cameraImg, renderedImg, mask)
                cameraImg = ImageProcessing.blendImages(renderedImg, cameraImg, mask)


                #drawing of the mesh and keypoints
                if drawOverlay:
                    drawPoints(cameraImg, shape2D.T)
                    drawProjectedShape(cameraImg, [mean3DShape, blendshapes], projectionModel, mesh, modelParams, lockedTranslation)

        writer.write(cameraImg)

        
        
    else:
        print("Stopping video writer")
        writer.release()
        cap.release()
        
        break
end_time = time.time()
print(end_time-start_time)