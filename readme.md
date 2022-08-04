# Pygame plane shooting game
Very simple tower defence game where you shoot down enemy planes in order to postpone the imminent invasion of your country.
## Hitting the planes
Aiming and shooting at a plane is pretty simple;
```
difference_x = self.enemy.pos[0] - self.pos[0] 
difference_y = self.enemy.pos[1] - self.pos[1]
# Plug the difference into this function to get the radians
angle = atan2(difference_y, difference_x)
# Convert the radians into an angle and return it
angle = degrees(angle)
```
However what if we want to hit a moving plane... there are a couple other things we have to add.
Of course we have to aim ahead of the plane. 
In order the figure out the needed offset, we have to find out how far the plane moves in the time that the bullet takes to travel from the turret to the plane.
We should start by getting the speed of both the enemy and the bullet.
### Find out the speed of the bullet
```
self.last_x, self.last_y = self.pos
		
self.pos = (self.pos[0] + (self.speed * cos(angle_in_radians)), self.pos[1] + (self.speed * sin(angle_in_radians)))

self.length_traveled = distance = sqrt((self.pos[0] - self.last_x)**2 + (self.pos[1] - self.last_y)**2)
```
Before we update the position of the bullet, we save it's position. Then we can get the distance between the saved position and the new position and find out how much it moves every frame. Multiplying it by the framerate (60 in this case) will get us pixels / second.
