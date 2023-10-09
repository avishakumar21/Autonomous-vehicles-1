from entities import RectangleEntity, CircleEntity, RingEntity
from geometry import Point

# For colors, we use tkinter colors. See http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

class Car(RectangleEntity):
    def __init__(self, ID, model, center: Point, heading: float, color: str = 'red', lane = 0):
        size = Point(4., 2.)
        movable = True
        friction = 0.06
        super(Car, self).__init__(center, heading, size, movable, friction)
        self.color = color
        self.collidable = True
        self.lane = lane   # added 
        self.sensor = True 
        self.ID = ID
        self.type = model
        # four lane highway, each lane is assigned a value
        # _______
        #    4
        # _______
        # _______
        #    3
        # _______
        # _______
        #    2
        # _______
        # _______
        #    1
        # _______
        # depending on whether the car merges left or right, we subtract or add 1 from self.lane
        
class Pedestrian(CircleEntity):
    def __init__(self, radius, ID, center: Point, heading: float, color: str = 'black'): 
        radius = radius
        movable = True
        friction = 0.2
        super(Pedestrian, self).__init__(center, heading, radius, movable, friction)
        self.color = color
        self.collidable = True
        self.sensor = False 
        self.ID = ID
        
class RectangleBuilding(RectangleEntity):
    def __init__(self, ID, center: Point, size: Point, color: str = 'gray26'):
        heading = 0.
        movable = False
        friction = 0.
        super(RectangleBuilding, self).__init__(center, heading, size, movable, friction)
        self.color = color
        self.collidable = True
        self.sensor = False 
        self.ID = ID
        
class CircleBuilding(CircleEntity):
    def __init__(self, center: Point, radius: float, color: str = 'gray26'):
        heading = 0.
        movable = False
        friction = 0.
        super(CircleBuilding, self).__init__(center, heading, radius, movable, friction)
        self.color = color
        self.collidable = True
        self.sensor = False

class RingBuilding(RingEntity):
    def __init__(self, center: Point, inner_radius: float, outer_radius: float, color: str = 'gray26'):
        heading = 0.
        movable = False
        friction = 0.
        super(RingBuilding, self).__init__(center, heading, inner_radius, outer_radius, movable, friction)
        self.color = color
        self.collidable = True
        self.sensor = False
        
class Painting(RectangleEntity):
    def __init__(self, center: Point, size: Point, color: str = 'gray26', heading: float = 0.):
        movable = False
        friction = 0.
        super(Painting, self).__init__(center, heading, size, movable, friction)
        self.color = color
        self.collidable = False
        self.sensor = False