from Mine3D import *
from Mine3D.prefabs.first_person_controller import FirstPersonController
from Mine3D.prefabs.health_bar import HealthBar
from Mine3D.prefabs.sky import Sky
from Mine3D.prefabs.draggable import Draggable
from Mine3D.PerlinNoise import PerlinNoise
from Mine3D.shaders import lit_with_shadows_shader


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

Cursor()





noise = PerlinNoise(octaves=2, seed=1)
freq = 20
amp = 10
terrain = Entity(model = None, collider = None)

class LoadingWheel(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.parent = camera.ui
        self.point = Entity(parent=self, model=Circle(24, mode='point', thickness=.03), color=color.light_gray, y=.75, scale=2, texture='circle')
        self.point2 = Entity(parent=self, model=Circle(12, mode='point', thickness=.03), color=color.light_gray, y=.75, scale=1, texture='circle')

        self.scale = .025
        self.text_entity = Text(world_parent=self, text='loading...', origin=(0,1.5), color=color.light_gray)
        self.y = -.25

        self.bg = Entity(parent=self, model='quad', scale_x=camera.aspect_ratio, color=color.black, z=1)
        self.bg.scale *= 400

        for key, value in kwargs.items():
            setattr(self, key ,value)
        


    def update(self):
        self.point.rotation_y += 5
        self.point2.rotation_y += 3





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
            model = 'quad',
            scale = (1.2, 0.32),
            position = (0, -0.36),
            color = color.gray,
            texture = "white_cube"
        )





# class arrow(Button):
#     def __init__(self):
#         super().__init__(
#             parent = scene,
#             model = 
#         )

class item(Draggable):
    def __init__(self, pos = (-0.4, -0.28)):
        super().__init__(
            parent = camera.ui, 
            model = "quad",
            color = color.red,
            position = pos,
            scale = (0.1, 0.1)
        )

    def drag(self):
        pass

    def drop(self):
        pass

class Grid(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            texture = "white_cube",
            texture_scale = (4, 7),
            scale = (1.1, 0.31),
            position = (0, -0.36)
        )


class arrow(Button):
    super().__init__(
        parent = scene,
        
    )

class Inventory(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            parent = camera.ui,
            model = Quad(radius=.015),
            texture = 'white_cube',
            texture_scale = (5,8),
            scale = (.5, .8),
            origin = (-.5, .5),
            position = (-0.9,.4),
            color = color.color(0,0,.1,.9),
            )

        for key, value in kwargs.items():
            setattr(self, key, value)


    def find_free_spot(self):
        for y in range(8):
            for x in range(5):
                grid_positions = [(int(e.x*self.texture_scale[0]), int(e.y*self.texture_scale[1])) for e in self.children]
                print(grid_positions)

                if not (x,-y) in grid_positions:
                    print('found free spot:', x, y)
                    return x, y


    def append(self, item, x=0, y=0):
        print('add item:', item)

        if len(self.children) >= 5*8:
            print('inventory full')
            error_message = Text('<red>Inventory is full!', origin=(0,-1.5), x=-.5, scale=2)
            destroy(error_message, delay=1)
            return

        x, y = self.find_free_spot()

        icon = Draggable(
            parent = self,
            model = 'quad',
            texture = item,
            color = color.white,
            scale_x = 1/self.texture_scale[0],
            scale_y = 1/self.texture_scale[1],
            origin = (-.5,.5),
            x = x * 1/self.texture_scale[0],
            y = -y * 1/self.texture_scale[1],
            z = -.5,
            )
        name = item.replace('_', ' ').title()

        if random.random() < .25:
            icon.color = color.gold
            name = '<orange>Rare ' + name

        icon.tooltip = Tooltip(name)
        icon.tooltip.background.color = color.color(0,0,0,.8)


        def drag():
            icon.org_pos = (icon.x, icon.y)
            icon.z -= .01   # ensure the dragged item overlaps the rest

        def drop():
            icon.x = int((icon.x + (icon.scale_x/2)) * 5) / 5
            icon.y = int((icon.y - (icon.scale_y/2)) * 8) / 8
            icon.z += .01

            # if outside, return to original position
            if icon.x < 0 or icon.x >= 1 or icon.y > 0 or icon.y <= -1:
                icon.position = (icon.org_pos)
                return

            # if the spot is taken, swap positions
            for c in self.children:
                if c == icon:
                    continue

                if c.x == icon.x and c.y == icon.y:
                    print('swap positions')
                    c.position = icon.org_pos


        icon.drag = drag
        icon.drop = drop


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
inventory = Inventory()

def add_item(add):
    inventory.append(add)
        #inventory.append(random.choice(('bag', 'bow_arrow', 'gem', 'orb', 'sword')))                                             



Health = HealthBar()
Minecraft.run()