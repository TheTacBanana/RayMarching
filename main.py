import pygame
from volume import *
from vec3 import *
from light import *

camPos = Vector3(0, 0, 0)
camForward = Vector3(1, 0, 0)
camRight = Vector3(0, 1, 0)
camUp = Vector3(0, 0, 1)
backgroundColour = Vector3(135,206,235)
distanceFog = 20

renderres = Vector3(250, 250, 128) # X Res, Y Res, Max Casts
volumes = [ WavyPlane(Vector3(0,0,-2), Vector3(155,155,155), Vector3(100, 100, 100))]
lights = [Light(Vector3(2,0,-1), 100, Vector3(253, 184, 19))]

#volumes.append(SmoothUnion(Sphere(Vector3(1, -0.1, 0), 0.2, Vector3(255, 0, 0)), Sphere(Vector3(1, 0.1, 0), 0.2, Vector3(255, 0, 0)), 0.1))
volumes.append(SmoothUnion(Sphere(Vector3(1, -0.1, 0), 0.2, Vector3(255, 0, 0)), Torus(Vector3(1, 0.1, 0), 0.2, 0.1,Vector3(255, 0, 0)), 0.1))
#volumes.append(WavySphere(Vector3(2, 0, 0), 0.5, 0.01, Vector3(255, 0, 0)))
#volumes.append(Sphere(Vector3(2, 0, 0), 0.2, Vector3(255, 0, 0)))
#volumes.append(Sphere(Vector3(2, 0, 1), 0.5, Vector3(255, 0, 0)))
#volumes.append(Plane(Vector3(0,0,3), Vector3(155,155,155), Vector3(100, 100, 100)))

window = pygame.display.set_mode((renderres.x, renderres.y))
pygame.display.set_caption('Ray Marching')

drawn = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                pygame.image.save(window, "ss.png")

    if drawn:
        pygame.time.delay(500)
        continue

    for y in range(renderres.y):
        ycam = (y - (renderres.y / 2)) / renderres.y
        for x in range(renderres.x):
            distTravelled = 0

            xcam = (x - (renderres.x / 2)) / renderres.x

            rayDir = camForward + (camRight * xcam) + (camUp * ycam)
            rayDir = rayDir.unit_vector()

            draw = False
            for s in range(renderres.z):
                volumeIndex = 0
                volumeDistance = 1000

                newPos = camPos + rayDir * distTravelled

                for v in range(len(volumes)):
                    newDist = volumes[v].SDF(newPos)
                    if newDist < volumeDistance:
                        volumeDistance = newDist
                        volumeIndex = v

                if volumeDistance < 0.01:
                    draw = True
                    break

                distTravelled += volumeDistance
                volumeIndex = 0 
                volumeDistance = 1000

            pos = camPos + rayDir * distTravelled
            if draw:
                rawcolour = volumes[volumeIndex].Colour(pos)
                normal = volumes[volumeIndex].Normal(pos)

                dot = (camPos - pos).unit_vector().dot(normal)
                normalshading = rawcolour * (0.5 + dot/2)

                #lightvalue = min(sum([i.TraceLight(pos, volumes, renderres.z) for i in lights]), 1)

                finalcolour = (normalshading.clamplerp(backgroundColour, distTravelled / distanceFog)).to_tuple()

                window.set_at((x, renderres.y - y), finalcolour)
            else:
                finalcolour = Vector3(255, 255, 255).clamplerp(backgroundColour, distTravelled / distanceFog).to_tuple()

                window.set_at((x, renderres.y - y), finalcolour)

            pygame.display.update()
    drawn = True