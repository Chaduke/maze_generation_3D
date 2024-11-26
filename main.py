# Maze Generation in 3D
# by Chad Dore' (Chaduke)
# https://chaduke.github.io/support-me
# 20240918

from libsgd import sgd
from maze import Maze
from player import Player

maze_width = 41
maze_depth = 41

m = Maze(maze_width,maze_depth,1)
m.visit(1,1)

# create the entrance
m.maze[(1,0)] = m.EMPTY
m.maze[(maze_width - 4,maze_depth-1)] = m.EMPTY

sgd.init()
sgd.createWindow(1920,1080,"Maze",sgd.WINDOW_FLAGS_FULLSCREEN)
env = sgd.loadCubeTexture("sgd://envmaps/grimmnight-cube.jpg", 4, 56)
sgd.setEnvTexture(env)
skybox = sgd.createSkybox(env)
light = sgd.createDirectionalLight()
sgd.turnEntity(light,-45,-45,0)
sgd.setAmbientLightColor(1,1,1,0.1)
m.create_blocks()
# create the floor
floor_material = sgd.loadPBRMaterial("sgd://materials/Tiles093_1K-JPG")
floor_mesh = sgd.createBoxMesh(0,-0.1,0,maze_width,0,maze_depth,floor_material)
sgd.transformTexCoords(floor_mesh,maze_width,maze_depth,0,0)
floor = sgd.createModel(floor_mesh)
sgd.moveEntity(floor,-0.5,0,-0.5)

p = Player()

sgd.enableCollisions(1,0,sgd.COLLISION_RESPONSE_SLIDE)
sgd.setMouseCursorMode(sgd.MOUSE_CURSOR_MODE_DISABLED)
loop = True
while loop:
    e = sgd.pollEvents()
    if e == 1 : loop = False
    if sgd.isKeyHit(sgd.KEY_ESCAPE) : loop = False
    p.update()
    sgd.updateColliders()
    sgd.renderScene()
    sgd.clear2D()
    sgd.draw2DText(str(sgd.getFPS()),5,5)
    m.draw2d(sgd.getWindowWidth() - (m.WIDTH * m.grid_size),0,p)
    sgd.present()
sgd.terminate()