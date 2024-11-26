from libsgd import sgd

# it looks like I was going to adapt this into a dungeon crawler type game but got sidetracked

class Player:
    def __init__(self):
        self.speed = 0.05
        self.health = 100
        self.camera = sgd.createPerspectiveCamera()
        self.pivot = sgd.createModel(0)
        self.collider = sgd.createSphereCollider(self.pivot,1,0.25)
        sgd.setEntityParent(self.camera, self.pivot)
        sgd.moveEntity(self.pivot, 1, 0.5, -1)
        sgd.turnEntity(self.pivot,0,180,0)
        # just an example of how you could adapt this
        self.monsters_killed = 0
        self.missiles_fired = 0
        self.damage_taken = 0
        self.level = 1
    def update(self):
        if self.health < 0:
            #_game.over = True
            self.health = 0

        # get keyboard input
        if sgd.isKeyDown(sgd.KEY_W) or sgd.isKeyDown(sgd.KEY_UP):
            sgd.moveEntity(self.pivot, 0, 0, self.speed)
        elif sgd.isKeyDown(sgd.KEY_S) or sgd.isKeyDown(sgd.KEY_DOWN):
            sgd.moveEntity(self.pivot, 0, 0, -self.speed)
        if sgd.isKeyDown(sgd.KEY_A) or sgd.isKeyDown(sgd.KEY_LEFT):
            sgd.moveEntity(self.pivot, -self.speed, 0, 0)
        elif sgd.isKeyDown(sgd.KEY_D) or sgd.isKeyDown(sgd.KEY_RIGHT):
            sgd.moveEntity(self.pivot, self.speed, 0, 0)

        # check bounds
        # if sgd.GetEntityX(self.pivot) < -50:
        #     sgd.SetEntityPosition(self.pivot, -50, 0.5, sgd.GetEntityZ(self.pivot))
        # if sgd.GetEntityZ(self.pivot) < -50:
        #     sgd.SetEntityPosition(self.pivot, sgd.GetEntityX(self.pivot),0.5, -50)
        # if sgd.GetEntityX(self.pivot) > 50:
        #     sgd.SetEntityPosition(self.pivot, 50, 0.5, sgd.GetEntityZ(self.pivot))
        # if sgd.GetEntityZ(self.pivot) > 50:
        #     sgd.SetEntityPosition(self.pivot, sgd.GetEntityX(self.pivot), 0.5,50)
        # if sgd.GetEntityY(self.pivot) < 0.5 or sgd.GetEntityY(self.pivot) > 0.5:
        #     sgd.SetEntityPosition(self.pivot, sgd.GetEntityX(self.pivot), 0.5, sgd.GetEntityZ(self.pivot))

        # mouse input
        sgd.turnEntity(self.pivot, 0, -sgd.getMouseVX() * 0.2, 0)
        sgd.turnEntity(self.camera, -sgd.getMouseVY() * 0.1, 0, 0)
        if sgd.getEntityRX(self.camera) < -7: sgd.setEntityRotation(self.camera, -7, 0, 0)
        if sgd.getEntityRX(self.camera) > 25: sgd.setEntityRotation(self.camera, 25, 0, 0)