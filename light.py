from vec3 import *

class Light():
    def __init__(self, pos, strength, colour):
        self.pos = pos
        self.strength = strength
        self.colour = colour

    def TraceLight(self, targetPos, volumes, steps):
        targetDistance = (targetPos - self.pos).magnitude()
        rayDir = (targetPos - self.pos).unit_vector()
        distTravelled = 0

        for _ in range(8 * steps):
            volumeDistance = 1000

            newPos = self.pos + rayDir * distTravelled

            for v in range(len(volumes)):
                newDist = volumes[v].SDF(newPos)
                if newDist < volumeDistance:
                    volumeDistance = newDist

            if (targetDistance - distTravelled < 0.1):
                return self.strength / (targetDistance ** 2)

            #print(volumeDistance)
            distTravelled += volumeDistance
            volumeDistance = 1000

        #print(distTravelled)
        return 0.35