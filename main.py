"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.

CS241
Nathan Taylor
"""
import arcade
import math
import random
from abc import abstractmethod
from abc import ABC

# These are Global constants to use throughout the game
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60
BULLET_SPIN = 100

SHIP_TURN_AMOUNT = 3
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5
                                                                                    
BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2

class Point:
    # This will initiate the point to be a float.
    def __init__ (self):
        self.x = 0.0
        self.y = 0.0
        
class Velocity:
    # This will initiate the velocity to be a float.
    
    def __init__(self):
        self.dx = 0.0
        self.dy = 0.0
        
class FlyingObject:
    
    def __init__(self,img):
        self.center = Point()
        self.velocity = Velocity()
        self.radius = 0.0
        self.alive = True
        
        self.angle = 0.0
        self.texture = arcade.load_texture(img)
        self.width = self.texture.width 
        self.height = self.texture.height 
    
    def advance(self):
        #This will advance the flying object
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
        
        self.is_off_screen()
        
       
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)
    
    def is_off_screen(self):
        """
        Will determine if the object is off screen and will send it to the other side
        allowing the objects to wrap around the screen
        """
        if (self.center.x > SCREEN_WIDTH):
            self.center.x = 0.0
        elif (self.center.x < 0.0):
            self.center.x = SCREEN_WIDTH
        elif (self.center.y > SCREEN_HEIGHT):
            self.center.y = 0.0
        elif (self.center.y < 0.0):
            self.center.y = SCREEN_HEIGHT
     
  
    
class Ship(FlyingObject):
    
    def __init__(self):
        """
        Initializes the Ship
        """
        super().__init__("Images/playerShip1_orange.png")
        self.speed = SHIP_THRUST_AMOUNT
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2
        self.radius = SHIP_RADIUS
        self.count = 0
        self.lives = 3
        self.charge = 100


    def ship_thrust(self): # Increases ships speed and moves it
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT 
        
    
    def ship_brake(self): # slows ship down

        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    
    def ship_right(self): # rotates ship
        self.angle -= SHIP_TURN_AMOUNT
    
    def ship_left(self): # rotates ship
        self.angle += SHIP_TURN_AMOUNT
        
    def hit(self):
        """
        Sets self.alive to False when the ship is hit
        """
        self.lives -= 1
        if self.lives > 0:
            super().__init__("Images/playerShip1_orange.png")
            self.radius = SHIP_RADIUS
            self.center.x = SCREEN_WIDTH / 2
            self.center.y = SCREEN_HEIGHT / 2
            self.count = 50
        else:
            self.alive = False
        
    def restart(self):
        """
        restarts the ship for the next level
        """
        
        super().__init__("Images/playerShip1_orange.png")
        
        self.center.x = SCREEN_WIDTH / 2
        self.center.y = SCREEN_HEIGHT / 2
        self.count = 50
        
        
class Bullet(FlyingObject):
    def __init__(self, Ship):
        """
        Initializes the  bullet
        """
        super().__init__("Images/laserBlue01.png")
        self.angle = Ship.angle
        self.velocity.dx = Ship.velocity.dx
        self.velocity.dy = Ship.velocity.dy
        self.center.x = Ship.center.x 
        self.center.y = Ship.center.y 
        self.radius = BULLET_RADIUS
        self.count = 0
              
    def fire(self):
        """
        Sets the velocity for the bullet
        """
        self.velocity.dx -= (math.sin(math.radians(self.angle)) *  BULLET_SPEED)
        self.velocity.dy += (math.cos(math.radians(self.angle)) * BULLET_SPEED)
        

class Asteroid(FlyingObject, ABC):
    """
    This class is for all the different types of asteroids.
    Each asteroid has a draw, hit, and rotate function.
    These functions will be passed down to each asteroid.
    """
    
    def __init__(self,img, spin):
        super().__init__(img)
        self.spin = spin
       
    @abstractmethod
    def hit(self, asteroids):
        pass
    
    def rotate(self): # not abstract the diffreent spin rates get passed in 
        self.angle += self.spin
    
class Large_rock(Asteroid):
    
    def __init__(self):
        """
        Initializes the Large asteroid
        """
        super().__init__("Images/meteorGrey_big1.png",BIG_ROCK_SPIN)
        self.angle = random.randint(0,360)
        self.radius = BIG_ROCK_RADIUS
        self.velocity.dx = math.cos(math.radians(self.angle)) * BIG_ROCK_SPEED
        self.velocity.dy = math.sin(math.radians(self.angle)) * BIG_ROCK_SPEED

        
    def hit(self, asteroids):
        """
        This function will return two medium asteroids and one small asteroid in the same
        location where the Large asteroid was hit
        """
        m = Medium_rock()
        m.center.x = self.center.x
        m.center.y = self.center.y
        m.velocity.dy = self.velocity.dy + 2
        m.velocity.dx = self.velocity.dx
        m.angle = self.angle 
        
        m1 = Medium_rock()
        m1.center.x = self.center.x
        m1.center.y = self.center.y
        m1.velocity.dy = self.velocity.dy - 2
        m1.velocity.dx = self.velocity.dx
        m.angle = self.angle
        
        s1 = Small_rock()
        s1.center.x = self.center.x
        s1.center.y = self.center.y
        s1.velocity.dx = self.velocity.dx + 5
        s1.velocity.dy = self.velocity.dy
        s1.angle = self.angle
        
        self.alive = False 
        asteroids.append(m)
        asteroids.append(m1)
        asteroids.append(s1)
        return 100

        
class Medium_rock(Asteroid):
    
    def __init__(self):
        """
        Initializes the Medium asteroid
        """
        super().__init__("Images/meteorGrey_med1.png",MEDIUM_ROCK_SPIN)
        self.angle = random.randint(0,360)
        self.radius = MEDIUM_ROCK_RADIUS
        self.velocity.dx = math.cos(math.radians(self.angle)) * BIG_ROCK_SPEED * 2
        self.velocity.dy = math.sin(math.radians(self.angle)) * BIG_ROCK_SPEED * 2
  
    def hit(self, asteroids):
        """
        This function will return two small asteroids in the same
        location where the medium asteroid was hit
        """
        s = Small_rock()
        s.center.x = self.center.x
        s.center.y = self.center.y
        s.velocity.dx = self.velocity.dx + 1.5
        s.velocity.dy = self.velocity.dy + 1.5
        s.angle = self.angle 
        
        s1 = Small_rock()
        s1.center.x = self.center.x
        s1.center.y = self.center.y
        s.velocity.dx = self.velocity.dx - 1.5
        s.velocity.dy = self.velocity.dy - 1.5
        s1.angle = self.angle 
         
        self.alive = False
        asteroids.append(s1)
        asteroids.append(s)
        return 250


class Small_rock(Asteroid):
    
    def __init__(self):
        """
        Initializes the small asteroid
        """
        super().__init__("Images/meteorGrey_small1.png",SMALL_ROCK_SPIN)
        self.radius = SMALL_ROCK_RADIUS
        self.angle = random.randint(0,360)
        self.velocity.dx = math.cos(math.radians(self.angle)) * BIG_ROCK_SPEED * 5
        self.velocity.dy = math.sin(math.radians(self.angle)) * BIG_ROCK_SPEED * 5

    def hit(self, asteroids):
        """
        When this rock dies it doesnt return anything. 
        """
        self.alive = False
        return 500
class Intro(arcade.View):
    
    def on_show(self):
        arcade.set_background_color(arcade.csscolor.BLACK)
        
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("ASTEROIDS", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.GOLD, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.show_view(game_view)
        
class GameOverView(arcade.View):
    """ View to show when game is over"""
    def __init__(self):
        super().__init__()
    
    def on_draw(self):
        end_text = "GAME OVER"
        arcade.draw_text(end_text, (SCREEN_WIDTH // 2 - 80), SCREEN_HEIGHT // 2, font_size=32, color=arcade.color.GOLD)
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.window.show_view(game_view)   
        
class Game(arcade.View):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__()
        #arcade.set_background_color(arcade.color.BLACK)

        self.held_keys = set()
        
        self.ship = Ship()
        
        self.asteroids = []
        
        self.bullets = []
        
        self.level = 1
        
        self.score = 0
        
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
               
        for n in range(INITIAL_ROCK_COUNT):
            new_asteroid = Large_rock()
            self.asteroids.append(new_asteroid)    
        

        # TODO: declare anything here you need the game class to track

    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """
        

        # clear the screen to begin drawing
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,SCREEN_WIDTH, SCREEN_HEIGHT,self.background)
        for bullet in self.bullets:
            if bullet.alive:
                bullet.draw()
                bullet.count += 1 #this is adding 1 to the number of frames the bullet has gone
        
                if bullet.count >= BULLET_LIFE: # If the count has gone more than 60 frames, it dies
                    bullet.alive = False

        self.draw_text()       
     
        if self.ship.alive:
       
            self.ship.draw()

        else:
            view = GameOverView()
            self.window.show_view(view)
        
        for asteroid in self.asteroids:
            asteroid.draw()
        
    def draw_text(self):
        asteroid_level = f"Level {self.level}"
        arcade.draw_text(asteroid_level, (SCREEN_WIDTH // 2 - 50), SCREEN_HEIGHT - 40, font_size=32, color=arcade.color.GOLD)
        arcade.draw_text(f"Score: {self.score}", (SCREEN_WIDTH // 2 - 50), SCREEN_HEIGHT - 72, font_size=32, color=arcade.color.GOLD)
        arcade.draw_text(repr(self.ship.charge), (10), SCREEN_HEIGHT - 20, font_size=16, color=arcade.color.GOLD)
        asteroid_count = f"Asteroids Left: {len(self.asteroids)}"
        arcade.draw_text(asteroid_count, (SCREEN_WIDTH - 150), SCREEN_HEIGHT - 20, font_size=16, color=arcade.color.GOLD)
        arcade.draw_text(repr(self.ship.lives), (5), 5, font_size=20, color=arcade.color.GOLD)
      

    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()
        self.check_collisions()
        

        if len(self.asteroids) == 0:
            self.level += 1
            
            for bullet in self.bullets:
                bullet.alive = False
                self.ship.hit()
                
                
            for n in range(self.level + INITIAL_ROCK_COUNT):
                new_asteroid = Large_rock()
                self.asteroids.append(new_asteroid)
                        
            
        self.ship.advance()
        if self.ship.count > 0:
            self.ship.count -= 1
        else:
            self.ship.count = 0

        
        for bullet in self.bullets:
            bullet.advance()
       
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.rotate()

    def check_collisions(self):
        """
        Checks to see if bullets have hit asteroids
        Updates the asteroid list
        Checks if asteroids have hit the ship
        :return:
        """
        if self.ship.count < 1:
            for asteroid in self.asteroids:
                if self.ship.alive and asteroid.alive:
                    too_close = self.ship.radius + asteroid.radius
                                
                    if (abs(self.ship.center.x - asteroid.center.x) < too_close and
                        abs(self.ship.center.y - asteroid.center.y) < too_close):
                        self.ship.hit()
                        self.score -= asteroid.hit(self.asteroids)
                        
                        
        
        for bullet in self.bullets:
            
           for asteroid in self.asteroids:
               # Make sure they are both alive before checking for a collision
               if bullet.alive and asteroid.alive:
                   too_close = bullet.radius + asteroid.radius
                   if (abs(bullet.center.x - asteroid.center.x) < too_close and
                    abs(bullet.center.y - asteroid.center.y) < too_close):
                       self.score += asteroid.hit(self.asteroids)
                       # its a hit!
                       bullet.alive = False
                       
        
        
        # Friendly Fire On           
#        for bullet in self.bullets:
#            if bullet.count > 15:
#                
#                if self.ship.alive and bullet.alive:
#                    too_close = self.ship.radius + bullet.radius
#                            
#                     if (abs(self.ship.center.x - bullet.center.x) < too_close and
#                        abs(self.ship.center.y - bullet.center.y) < too_close):
#                        self.ship.hit()
#                        
                
                
        self.cleanup_zombies()

    def cleanup_zombies(self):
        """
        Removes any dead bullets or targets from the list.
        :return:
        """
        for bullet in self.bullets:
            if not bullet.alive:
                self.bullets.remove(bullet)

        for asteroid in self.asteroids:
            if not asteroid.alive:
                self.asteroids.remove(asteroid)        
        
                
                        

    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
      
        if arcade.key.LEFT in self.held_keys:
            self.ship.ship_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.ship_right()

        if arcade.key.UP in self.held_keys:
            self.ship.ship_thrust()
            

        if arcade.key.DOWN in self.held_keys:
            self.ship.ship_brake()

        # Machine gun mode...
            
        if self.ship.charge > 0:
           if arcade.key.X  in self.held_keys:
                self.ship.charge -= 1
                new_bullet = Bullet(self.ship)
                new_bullet.fire()
                self.bullets.append(new_bullet)
        


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                new_bullet = Bullet(self.ship)
                new_bullet.fire()
                self.bullets.append(new_bullet)

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT)
start_view = Intro()
window.show_view(start_view)
arcade.run()
