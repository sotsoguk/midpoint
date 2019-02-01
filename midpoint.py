import os
import random
from PIL import Image, ImageDraw
import bisect
import itertools
import math

def computeMidpoint(start, end, damp, displacement, numIterations, width, height):

    points = [start, end]
    for it in range(0, numIterations):
        newPoints = []
        for i in range(len(points) - 1):
            mid = list(map(lambda x: (points[i][x] + points[i+1][x]) / 2, [0,1]) )
            mid[1] += random.choice([-displacement, displacement])
            newPoints.append(mid)
        for p in newPoints:
            bisect.insort(points,p)
        displacement /= 2
    return points

def computeMidpointOrth(start, end, damp, displacement, numIterations, width, height):

    points = [start, end]
    for it in range(0, numIterations):
        newPoints = []
        for i in range(len(points) - 1):
            mid = list(map(lambda x: (points[i][x] + points[i+1][x]) / 2, [0,1]) )
            # compute orthognal direction
            d = [points[i][1] - points[i+1][1], points[i+1][0] - points[i][0]]
            #print(d)
            invSqrt = (d[0]*d[0]+d[1]*d[1]) ** (-0.5)
            sc = random.choice([displacement,-displacement]) * invSqrt
            dsc = [i*sc for i in d]
            mid[0]+= dsc[0]
            mid[1]+= dsc[1]
            #print(dLen,sc,mid)
            #mid[1] += random.choice([-displacement, displacement])
            newPoints.append(mid)
        for p in newPoints:
            bisect.insort(points,p)
        displacement *= 2**(-damp)
       
     # close polygon
    startPoint = [start[0],height]
    endPoint = [end[0],height]
    points.insert(0,startPoint)
    points.append(endPoint)
    return points

def main():
    # Terrain dimension
    width = 1200
    height = 600
    filename = 'test2o.png'

    lines = (computeMidpointOrth([0,300],[1200,300],1.2,90,16,width,height ))

    scene = Image.new('RGBA', (width, height), "white")
    sceneDraw = ImageDraw.Draw(scene)
    # lines.insert(0,[0,600])
    # lines.append([1200,600])
    sceneDraw.polygon(list(itertools.chain.from_iterable(lines)),fill=(100,0,255,127))#,outline=(0,255,0,255))

    # Save image
    print(os.getcwd())
    scene.save(os.getcwd() + '/' + filename)
    
    

if __name__ == "__main__":
    main()