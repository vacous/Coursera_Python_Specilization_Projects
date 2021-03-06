# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0

ship_action1 = 'none'
ship_action2 = 'none'
ship_action3 = 'none'

ROCK_ANG_VEL=[-100,-10,-0.3,-0.1,
        0,
        0.1,0.3,10,100]
ROCK_VEL=[-5,5]
ROCK_ANG=[-4,4]

missile_pos=[0,0]
missile_vel=[0,0]
vel_factor = 3
vel_ini = 5


num_lives = 3
num_score = 0
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 10,60)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 80)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
ship_thrust_sound.set_volume(0.5)
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        
   
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = 0
        self.angle = angle
        self.angle_vel = 0.1
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        if self.thrust == 0:
            canvas.draw_image(ship_image, self.image_center, (90, 90),
                              (self.pos[0], self.pos[1]), self.image_size,
                              self.angle)
        else:
            canvas.draw_image(ship_image, [self.image_center[0]+self.image_size[0],self.image_center[1]],
                               self.image_size,
                              (self.pos[0], self.pos[1]), (90, 90),
                             self.angle)
    
    def get_info(self):
        return [self.pos, self.angle]
        print ''
        print 'Position: '+str(self.pos)
        print 'Velocity: '+str(self.vel)
        print 'Angle: '+str(self.angle)
        print 
        print '____________________________________'
        
    def update(self,action1, action2,action3):
        friction_convert = 0.05
        
        
        if action1 == 'move' or 'None':
            decelerate =[ -friction_convert * self.vel[0]
                         ,-friction_convert * self.vel[1]  ] 
            self.vel = [self.vel[0]+decelerate[0]
                        ,self.vel[1]+decelerate[1] ]
            self.pos = [self.pos[0]+self.vel[0], self.pos[1]+self.vel[1]]
            
            # The position reset to the other end when outside of the canvas
            self.pos=[self.pos[0]%WIDTH, self.pos[1]%HEIGHT]
            #print 'Friction: '+str(decelerate)
            
            if action1 == 'move':
                self.thrust = 0.5
                acc = [self.thrust * math.cos(self.angle),
                       self.thrust * math.sin(self.angle)]
                self.vel=[self.vel[0]+acc[0], self.vel[1]+acc[1]]
                self.pos=[self.pos[0]+self.vel[0], self.pos[1]+self.vel[1]]
                # The position reset to the other end when outside of the canvas
                self.pos=[self.pos[0]%WIDTH, self.pos[1]%HEIGHT]
                #print str(acc)
                #print str(self.angle)
                
                ship_thrust_sound.play()
                
            elif action1 == 'none':
                self.thrust = 0 
                ship_thrust_sound.rewind()
                
                
            if action2 == 'rotate clock':
                self.angle = self.angle - self.angle_vel
          
            elif action2 == 'rotate counter':
                self.angle = self.angle + self.angle_vel

            elif action2 == 'none':
                self.angle = self.angle
                
            if action3 == 'shot':
                global  a_missile
                missile_pos = [self.pos[0] + self.image_size[0]/2.0 * math.cos(self.angle),
                              self.pos[1] + self.image_size[0]/2.0 * math.sin(self.angle)]
                
                missile_vel = [self.vel[0]*vel_factor+vel_ini* math.cos(self.angle),
                           self.vel[1]*vel_factor+vel_ini* math.sin(self.angle)]
                print missile_vel
                a_missile = Sprite( missile_pos, missile_vel,
                   0, 0, missile_image, missile_info, missile_sound)   
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            self.sound = sound 
        else: 
            self.sound = 'None'

            
                    
   
    def draw(self, canvas):
        if self.lifespan >=0:
        
            canvas.draw_image(self.image, self.image_center, self.image_size,
                                (self.pos[0], self.pos[1]), (self.radius, self.radius),
                                self.angle)
            if self.sound != 'None':
                    self.sound.play()
                
            self.lifespan -= 1
           
                
            
            
            
            
            
    def update(self):
        self.angle = self.angle + self.angle_vel  
        self.pos = [self.pos[0]+self.vel[0] , self.pos[1] + self.vel[1] ]
        self.pos=[self.pos[0]%WIDTH, self.pos[1]%HEIGHT]

        
        
        
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    
    
    

    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update(ship_action1,ship_action2, ship_action3)
    a_rock.update()
    
    
    
    
    a_missile.update()
          
    canvas.draw_text('Lives: '+str(num_lives), (650, 50), 20, 'Red')
    canvas.draw_text('Score: '+str(num_score), (50, 50), 20, 'Red')
    
    

        
    
    
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    spawn_pos= [ random.randrange(0,WIDTH), 
                random.randrange(0,HEIGHT)]
    
    spawn_vel=[random.randrange(ROCK_VEL[0],ROCK_VEL[1]), 
              random.randrange(ROCK_VEL[0],ROCK_VEL[1])]

    spawn_angle = random.randrange(ROCK_ANG[0],ROCK_ANG[1])
    
    spawn_angle_vel = random.choice(ROCK_ANG_VEL)
    
    a_rock = Sprite(spawn_pos, spawn_vel, spawn_angle,
                    spawn_angle_vel, asteroid_image, asteroid_info)
    # test print 
    #print '' 
    #print 'Rock velocity: '+str(spawn_vel)
    #print 'Rock angle: '+str(spawn_angle)
    #print 'Rock angle velocity : '+str(spawn_angle_vel)
    #print '___________________________________________'
    
# key handler
def keydown(key):
    global ship_action1, ship_action2, ship_action3
    if key==simplegui.KEY_MAP["left"]:
        ship_action2 = 'rotate clock'
    elif key==simplegui.KEY_MAP["right"]:
        ship_action2 = 'rotate counter'
    elif key==simplegui.KEY_MAP["up"]:
        ship_action1 = 'move'
    elif key==simplegui.KEY_MAP["space"]:
        ship_action3 = 'shot' 
        print missile_pos #temp

def keyup(key):
    global ship_action1, ship_action2, ship_action3
    if key==simplegui.KEY_MAP["left"]:
        ship_action2 = 'none'
    elif key==simplegui.KEY_MAP["right"]:
        ship_action2 = 'one'
    elif key==simplegui.KEY_MAP["up"]:
        ship_action1 = 'none'
    elif key==simplegui.KEY_MAP["space"]:
        ship_action3 = 'none'
        print missile_pos #temp
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)


frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [0, 0]
                , 0, 0, asteroid_image, asteroid_info)

a_missile = Sprite( [0,0], missile_vel,
                   0, 0, missile_image, missile_info)
    


# register handlers
frame.set_draw_handler(draw)

# add buttons 



timer = simplegui.create_timer(1000.0, rock_spawner)
# get things rolling
timer.start()
frame.start()