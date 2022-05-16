import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np



def setupSelfDefineFBO(program,image):

    fbWidth, fbHeight = image.width, image.height

    # Setup framebuffer
    framebuffer = glGenFramebuffers (1)
    glBindFramebuffer(GL_FRAMEBUFFER, framebuffer)

    # Setup colorbuffer
    colorbuffer = glGenRenderbuffers (1)
    glBindRenderbuffer(GL_RENDERBUFFER, colorbuffer)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_RGBA, fbWidth, fbHeight)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, colorbuffer)

    # Setup depthbuffer
    depthbuffer = glGenRenderbuffers (1)
    glBindRenderbuffer(GL_RENDERBUFFER,depthbuffer)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH_COMPONENT, fbWidth, fbHeight)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_RENDERBUFFER, depthbuffer)

    # check status
    status = glCheckFramebufferStatus (GL_FRAMEBUFFER)
    if status != GL_FRAMEBUFFER_COMPLETE:
        print( "Error in framebuffer activation")

    glViewport(0, 0, fbWidth, fbHeight)

    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, aTexture)
    loc = glGetUniformLocation(program, "Texture")
    glUniform1i(loc, 0)

    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
    saveImageFromFBO(fbWidth, fbHeight)

    glBindFramebuffer(GL_FRAMEBUFFER, GL_NONE)
    glViewport(0, 0, 512, 512)