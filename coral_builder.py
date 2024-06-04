# Inspired by Recursion & Branching MEL Tutorial by Malcolm Kesson
# https://www.fundza.com/mel/tree/tree.html [Last accessed on 9 January 2024]

import random

import maya.cmds as cmds
import math
import numpy as np

# Unit vector
def norm(vec) :
    return vec / np.linalg.norm(vec)

# Reflect vector across another vector
def reflect(i, n) :
    i = norm(i)
    n = norm(n)
    return i - 2 * np.dot(i, n) * n

# Generate a vector on a circle
def vectorOnCircle(radius) :
    # find a random vector within 2 * radius square
    x = random.uniform(-radius, radius)
    z = random.uniform(-radius, radius)
    vec = [x, 0, z]

    vector = np.array(vec)
    vector = norm(vector)
    vector = vector * radius
    vector = np.array(vector)

    return vector


# Coral generation recursion function
def generateCoral(depth, base, growthDir, branchAngle, branchLen, branchWidth, lengthCoof) :

    # Add hemisphere on the tip
    if depth < 0 :
        cmds.polySphere(n='branchTip1', ax=growthDir, r=branchWidth)
        cmds.move(base[0], base[1], base[2], absolute=True)
        return

    # Calculate branch direction
    rad = branchLen * math.sin(math.radians(branchAngle))
    branchDir = vectorOnCircle(rad)
    branchDir = branchDir + branchLen * math.cos(math.radians(branchAngle)) * np.array([0.0, 1.0, 0.0])

    # Make sure branch points outwards
    if np.dot(branchDir, growthDir) < 0 :
        branchDir = -branchDir

    end = base + branchDir

    # Create the first branch
    cmds.polyCylinder(n='coralBranch_A1', ax=branchDir.tolist(), r=branchWidth, h=branchLen, sx=20, sy=20)
    baseOffset = base + 0.5 * branchDir
    cmds.move(baseOffset[0], baseOffset[1], baseOffset[2], absolute=True)

    generateCoral(depth - 1, end, branchDir, branchAngle, branchLen * lengthCoof, branchWidth, lengthCoof)

    # Calculate second branch direction
    branchDirB = reflect(-branchDir, growthDir)
    branchDirB = branchDirB * branchLen
    endB = base + branchDirB

    # Create the second branch
    cmds.polyCylinder(n='coralBranch_B1', ax=branchDirB.tolist(), r=branchWidth, h=branchLen, sx=20, sy=20)
    baseOffsetB = base + 0.5 * branchDirB
    cmds.move(baseOffsetB[0], baseOffsetB[1], baseOffsetB[2], absolute=True)

    generateCoral(depth - 1, endB, branchDirB, branchAngle, branchLen * lengthCoof, branchWidth, lengthCoof)

# Entry function to generate coral
def coralGenerator(depth, begin, dir, angle, len, width, lengthCoof) :
    generateCoral(depth, begin, dir, angle, len, width, lengthCoof)
    cmds.select( 'coralBranch_A*', 'coralBranch_B*', 'branchTip*' )
    cmds.polyUnite( n="proceduralCoral1" )
    cmds.delete(constructionHistory = True)

# execute

# This is some examples of parameters that generate some nice corals

begin = np.array([5.0, 0.0, 5.0])
dir = np.array([0.0, 1.0, 0.0])
angle = 10.0
len = 3.0
width = 0.1
lengthCoof = 0.7
depth = 4
coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)

begin = np.array([10.0, 0.0, -10.0])
angle = 40.0
len = 5.0
width = 0.5
lengthCoof = 0.6
depth = 7
coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)

begin = np.array([-5.0, 0.0, 5.0])
angle = 25.0
len = 3.0
width = 0.3
lengthCoof = 0.65
depth = 5
coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)

begin = np.array([-10.0, 0.0, -10.0])
angle = 25.0
len = 5.0
width = 0.3
lengthCoof = 0.65
depth = 5
coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)

# Bellow is the settings for creating multiple instances of different coral
# types I've used to generate most of the corals I need for my scene at once

# begin = np.array([0.0, 0.0, 0.0])
# dir = np.array([0.0, 1.0, 0.0])
# angle = 10.0
# len = 3.0
# width = 0.1
# lengthCoof = 0.7
# depth = 4
# for i in range(20):
#     coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)


# angle = 30.0
# len = 4.0
# width = 0.5
# lengthCoof = 0.7
# depth = 4
# for i in range(5):
#     coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)

# angle = 40.0
# len = 5.0
# width = 0.5
# lengthCoof = 0.6
# depth = 7
# for i in range(3):
#     coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)


# angle = 25.0
# len = 3.0
# width = 0.3
# lengthCoof = 0.65
# depth = 5
# for i in range(10):
#     coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)

# angle = 25.0
# len = 5.0
# width = 0.3
# lengthCoof = 0.65
# depth = 5
# for i in range(15):
#     coralGenerator(depth, begin, dir, angle, len, width, lengthCoof)
