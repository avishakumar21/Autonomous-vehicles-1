import numpy as np
from world import World
from agents import Car, RectangleBuilding, Pedestrian, Painting
from geometry import Point
import time
import csv
from random import *
import random as r

'''

ID 
100 :  Top Grass
200 :  Bottom Grass
300 :  Animal crossing
400 :  Pothole
1   :  Red Car
2   :  Black Car
3   :  Blue Car 
4   :  Purple Car
5   :  Yellow Car
6   :   Pink Car 

'''
human_controller = False

# NOTE: pressing alt pauses the simulation 

dt = 0.1  # time steps in terms of seconds. In other words, 1/dt is the FPS.
w = World(dt, width=240, height=120, ppm=6)  # The world is 240 meters by 120 meters. ppm is the pixels per meter.
# All velocities should be multiplied by the ppm in order to get the real-world m/s measurement of the cars max_speed. 

# A Painting object is a rectangle that the vehicles cannot collide with. So we use them for the sidewalks.
# A RectangleBuilding object is also static -- it does not move. But as opposed to Painting, it can be collided with.
# For both of these objects, we give the center point and the size.
w.add(RectangleBuilding('100', Point(80, 100), Point(280, 50),
                        'green'))  # The RectangleBuilding is then on top of the sidewalk, with some margin.
w.add(RectangleBuilding('200', Point(80, 30), Point(280, 50), 'green'))

# shoulder lane 
w.add(Painting(Point(18, 75), Point(400, 0.5), 'white'))
w.add(Painting(Point(18, 55), Point(400, 0.5), 'white'))

# three lanes
# 8 is x coordinate, 60 is y coordinate, 5 is length of line, 1 is width of line 

w.add(Painting(Point(8, 70), Point(5, 1), 'white'))
w.add(Painting(Point(18, 70), Point(5, 1), 'white'))
w.add(Painting(Point(28, 70), Point(5, 1), 'white'))
w.add(Painting(Point(38, 70), Point(5, 1), 'white'))
w.add(Painting(Point(48, 70), Point(5, 1), 'white'))
w.add(Painting(Point(58, 70), Point(5, 1), 'white'))
w.add(Painting(Point(68, 70), Point(5, 1), 'white'))
w.add(Painting(Point(78, 70), Point(5, 1), 'white'))
w.add(Painting(Point(88, 70), Point(5, 1), 'white'))
w.add(Painting(Point(98, 70), Point(5, 1), 'white'))
w.add(Painting(Point(108, 70), Point(5, 1), 'white'))
w.add(Painting(Point(118, 70), Point(5, 1), 'white'))
w.add(Painting(Point(128, 70), Point(5, 1), 'white'))
w.add(Painting(Point(138, 70), Point(5, 1), 'white'))
w.add(Painting(Point(148, 70), Point(5, 1), 'white'))
w.add(Painting(Point(158, 70), Point(5, 1), 'white'))
w.add(Painting(Point(168, 70), Point(5, 1), 'white'))
w.add(Painting(Point(178, 70), Point(5, 1), 'white'))
w.add(Painting(Point(188, 70), Point(5, 1), 'white'))
w.add(Painting(Point(198, 70), Point(5, 1), 'white'))
w.add(Painting(Point(208, 70), Point(5, 1), 'white'))

w.add(Painting(Point(8, 65), Point(5, 1), 'white'))
w.add(Painting(Point(18, 65), Point(5, 1), 'white'))
w.add(Painting(Point(28, 65), Point(5, 1), 'white'))
w.add(Painting(Point(38, 65), Point(5, 1), 'white'))
w.add(Painting(Point(48, 65), Point(5, 1), 'white'))
w.add(Painting(Point(58, 65), Point(5, 1), 'white'))
w.add(Painting(Point(68, 65), Point(5, 1), 'white'))
w.add(Painting(Point(78, 65), Point(5, 1), 'white'))
w.add(Painting(Point(88, 65), Point(5, 1), 'white'))
w.add(Painting(Point(98, 65), Point(5, 1), 'white'))
w.add(Painting(Point(108, 65), Point(5, 1), 'white'))
w.add(Painting(Point(118, 65), Point(5, 1), 'white'))
w.add(Painting(Point(128, 65), Point(5, 1), 'white'))
w.add(Painting(Point(138, 65), Point(5, 1), 'white'))
w.add(Painting(Point(148, 65), Point(5, 1), 'white'))
w.add(Painting(Point(158, 65), Point(5, 1), 'white'))
w.add(Painting(Point(168, 65), Point(5, 1), 'white'))
w.add(Painting(Point(178, 65), Point(5, 1), 'white'))
w.add(Painting(Point(188, 65), Point(5, 1), 'white'))
w.add(Painting(Point(198, 65), Point(5, 1), 'white'))
w.add(Painting(Point(208, 65), Point(5, 1), 'white'))

w.add(Painting(Point(8, 60), Point(5, 1), 'white'))
w.add(Painting(Point(18, 60), Point(5, 1), 'white'))
w.add(Painting(Point(28, 60), Point(5, 1), 'white'))
w.add(Painting(Point(38, 60), Point(5, 1), 'white'))
w.add(Painting(Point(48, 60), Point(5, 1), 'white'))
w.add(Painting(Point(58, 60), Point(5, 1), 'white'))
w.add(Painting(Point(68, 60), Point(5, 1), 'white'))
w.add(Painting(Point(78, 60), Point(5, 1), 'white'))
w.add(Painting(Point(88, 60), Point(5, 1), 'white'))
w.add(Painting(Point(98, 60), Point(5, 1), 'white'))
w.add(Painting(Point(108, 60), Point(5, 1), 'white'))
w.add(Painting(Point(118, 60), Point(5, 1), 'white'))
w.add(Painting(Point(128, 60), Point(5, 1), 'white'))
w.add(Painting(Point(138, 60), Point(5, 1), 'white'))
w.add(Painting(Point(148, 60), Point(5, 1), 'white'))
w.add(Painting(Point(158, 60), Point(5, 1), 'white'))
w.add(Painting(Point(168, 60), Point(5, 1), 'white'))
w.add(Painting(Point(178, 60), Point(5, 1), 'white'))
w.add(Painting(Point(188, 60), Point(5, 1), 'white'))
w.add(Painting(Point(198, 60), Point(5, 1), 'white'))
w.add(Painting(Point(208, 60), Point(5, 1), 'white'))

# A Car object is a dynamic object -- it can move. We construct it using its center location and heading angle.
# np/pi controls the orientation of the vehicle 
# since we want all the cars facing horizontal direction, we will set to np.pi
# if we wanted them going verticle (for intersection scenario), we will set to np.pi/2


# For the animal crossing scenario 
# It is a "circle" object rather than a rectangle.
# NOTE: might need to create green sidewalk in order for the animal to cross the street and enter grass without "collison"
'''p1 = Pedestrian(0.5, '300', Point(60,56), np.pi/2)
p1.max_speed = 10.0 # We can specify min_speed and max_speed (m/s)
w.add(p1)'''

# For the pothole scenario 
# creating a rectangle object in middle of lane, will cause a collision
'''p2 = Pedestrian(0.5, '400', Point(60, 57), np.pi / 2)
p2.max_speed = 0.0  # We can specify min_speed and max_speed (m/s)
w.add(p2)'''

# For the emergency responder scenario


p3 = Pedestrian(1.5, '500', Point(60, 57), 2*np.pi)
p3.max_speed = 15  # We can specify min_speed and max_speed (m/s)
w.add(p3)


# randomly generate speed for each vehicle
# max speed = 100km/hour  --> 28 m/s
# range +- 21.6 km/hour --> 6 m/s 

speedLimit = 28
speedRange = 2

# the second parameter is the type of the vehicle 
# 'H' is human model
# 'A' is autonomous model with V2V
# 'V' is autonomous model without V2V

# initialize the first car 
c1 = Car('1', 'H', Point(120, 62.5), np.pi, 'black', 2)
v1 = speedLimit + randint(-speedRange, speedRange)
c1.velocity = Point(v1, 0)
w.add(c1)

# initialize the second car 
c2 = Car('2', 'H', Point(140, 57), np.pi, 'blue', 1)
v2 = speedLimit + randint(-speedRange, speedRange)
c2.velocity = Point(v2, 0)
w.add(c2)

# initialize the third car 
c3 = Car('3', 'H', Point(130, 72.5), np.pi, 'purple', 4)
v3 = speedLimit + randint(-speedRange, speedRange)
c3.velocity = Point(v3, 0)
w.add(c3)

# initialize the fourth car 
c4 = Car('4', 'H', Point(110, 68), np.pi, 'yellow', 3)
v4 = speedLimit + randint(-speedRange, speedRange)
c4.velocity = Point(v4, 0)
w.add(c4)

# initalize fifth car
c5 = Car('5', 'H', Point(160, 68), np.pi, 'pink', 3)
v5 = speedLimit + randint(-speedRange, speedRange)
c5.velocity = Point(v5, 0)
w.add(c5)

w.render()  # This visualizes the world we just constructed.

cID = 5;
COLORS = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1']

lanes = [57.5,62.5,67.5,72.5]
if not human_controller:
    #p1.set_control(0, 0.4) # The pedestrian will have 0 steering and 0.22 throttle. So it will not change its direction.
    #p2.set_control(0, 0)
    p3.set_control(0, 4)
    c1.set_control(0, 0)
    c2.set_control(0, 0)
    c3.set_control(0, 0)
    c4.set_control(0, 0)
    c5.set_control(0, 0)

    #w.makeFile()

    for k in range(200):
        t = randint(16,21)
        if k % t == 0:
            model = 1 #r.randint(0, 2)
            # for randomly generating states
            if model == 0:
                currState = 'A'
            elif model == 1:
                currState = 'H'
            else:
                currState = 'V'
            # currState = 'V'
            currColor = r.choice(COLORS)
            laneSelection = r.choice(lanes)
            if 55 < laneSelection < 60:
                currLane = 1
            elif 60 < laneSelection < 65:
                currLane = 2
            elif 65 < laneSelection< 70:
                currLane = 3
            else:
                currLane = 4
            cTemp = Car(str(cID + 1), currState, Point(240, laneSelection), np.pi, currColor, currLane)
            cID += 1
            vTemp = speedLimit + randint(-speedRange, speedRange)
            cTemp.velocity = Point(vTemp, 0)
            w.add(cTemp)
            cTemp.set_control(0, 0)
        
        # Human Drivers
        # does not change lanes
        w.humanCollisionAvoidance()

        # Autonomous Vehicle Model 
        w.autonomousCollisionAvoidance()
        w.autonomousCollisionAvoidanceNoV2V()
        totalCollisions = w.collision_exists() 

        # Saftey : counter for collision
        w.updateGlobalInformation()


        w.delete()
        w.tick()  # This ticks the world for one time step (dt second)
        w.render()
        time.sleep(dt / 4)  # Let's watch it 4x

