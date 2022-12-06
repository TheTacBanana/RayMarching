#from vec3 import *

class Light():
    def __init__(self, pos, strength, colour):
        self.pos = pos
        self.strength = strength
        self.colour = colour

    def TraceLight(self, targetPos, volumes, steps):
        targetDistance = (targetPos - self.pos).magnitude()
        rayDir = (targetPos - self.pos).unit_vector()
        distTravelled = 0

        contribution = 1

        for _ in range(2 * steps):
            if (distTravelled > targetDistance - 0.01):
                lightRadius = 800
                fadeRatio = 1 - min(max(targetDistance / lightRadius, 0), 1)

                distanceFactor = fadeRatio ** 2

                print(contribution * distanceFactor)
                return contribution * distanceFactor

            volumeDistance = 1000

            newPos = self.pos + rayDir * distTravelled

            for v in range(len(volumes)):
                newDist = volumes[v].SDF(newPos)
                if newDist < volumeDistance:
                    volumeDistance = newDist

            if (volumeDistance <= 0):
                return 0

            distTravelled += volumeDistance

            if (volumeDistance < 0.1):
                contribution = max(0, contribution - volumeDistance)

            volumeDistance = 1000

        return 0