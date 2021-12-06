from Mine3D import *
from Mine3D.prefabs.first_person_controller import FirstPersonController
from Mine3D.prefabs.health_bar import HealthBar
from Mine3D.prefabs.sky import Sky
from Mine3D.prefabs.draggable import Draggable
from Mine3D.PerlinNoise import PerlinNoise

Minecraft = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture  = load_texture('assets/dirt_block.png')
sky_texture   = load_texture('assets/skybox.png')
arm_texture   = load_texture('assets/arm_texture.png')
punch_sound   = Audio('assets/punch_sound', loop = False, autoplay = False)
block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False
mouse.visible = True

noise = PerlinNoise(octaves=2, seed=1999999999999999999)
freq = 24
amp = 5
terrain = Entity(model = None, collider = None)

def update():
    global  block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
         hand1.active()
    else:
         hand1.active()

    if held_keys['1']:block_pick=1
    if held_keys['2']:block_pick=2
    if held_keys['3']:block_pick=3
    if held_keys['4']:block_pick=4



class Hand(Entity):
    def __init__(self, roat, pos):
        super().__init__(
            parent = camera.ui,
            model='assets/arm',
            texture = arm_texture,
            scale = 0.2,
            roatition = Vec3(150, -10, 0),
            position = Vec2(0.4, -0.6),
        )

    def active(self):
        position = Vec2(0.3, -0.5),

    def passive(self):
        position = Vec2(0.4, -0.6),


class BG(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
        )


class Voxel(Button):
    def __init__(self, pos = (0, 0, 0), texture = brick_texture):
        super().__init__(
            parent = scene,
            position = pos,
            model = "assets/block",
            orgin_y = 0.5,
            texture = texture,
            color = color.white,
            highlight_color = color.azure,
            collider = "box",
            scale = 0.5,

        )
    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                if block_pick  == 1: Voxel(pos=self.position + mouse.normal)
                if block_pick  == 2: Voxel(pos=self.position + mouse.normal ,texture=stone_texture)
                if block_pick  == 3: Voxel(pos=self.position + mouse.normal ,texture=grass_texture)
                if block_pick  == 4: Voxel(pos=self.position + mouse.normal ,texture=dirt_texture)

            if key == "right mouse down":
                punch_sound.play()
                destroy(self)

for z in range(20):
    for x in range(20):
        voxel = Voxel(pos=(x, 0, z))
        y = floor(noise([voxel.x/freq, voxel.z/freq]) * amp)
        voxel.y = y
        voxel.parent = terrain


for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -1, fz))


for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -2, fz))

for z in range(20):
    for x in range(20):
        voxel = Voxel(pos=(x, -3, z))

for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -4, fz))


for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -5, fz))


for z in range(20):
    for x in range(20):
        voxel = Voxel(pos=(x, -6, z))

for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -7, fz))


for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -8, fz))

for fz in range(20):
    for fx in range(20):
        voxel = Voxel(pos=(fx, -9, fz))

for z in range(20):
    for x in range(20):
        voxel = Voxel(pos=(x, -10, z))

terrain.combine()
terrain.collider = 'mesh'
terrain.texture = voxel.texture

player = FirstPersonController()
sky = Sky()
hand1 = Hand(roat = Vec3(150, -10, 0), pos = Vec2(0.4, -0.6))
Health = HealthBar()
Minecraft.run()