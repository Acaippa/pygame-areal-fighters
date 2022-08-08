# Pygame plane shooting game
Very simple tower defense game where you shoot down enemy planes to postpone the imminent invasion of your country.
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
However what if we want to hit a moving plane... there are a couple of other things we have to add.
Of course, we have to aim ahead of the plane. 
In order the figure out the needed offset, we have to find out how far the plane moves in the time that the bullet takes to travel from the turret to the plane.
We should start by getting the speed of both the enemy and the bullet.

### Find out the speed of the bullet
```
self.last_x, self.last_y = self.pos
		
self.pos = (self.pos[0] + (self.speed * cos(angle_in_radians)), self.pos[1] + (self.speed * sin(angle_in_radians)))

self.length_traveled = distance = sqrt((self.pos[0] - self.last_x)**2 + (self.pos[1] - self.last_y)**2)
```
Before we update the position of the bullet, we save its position. Then we can get the distance between the saved position and the new position and find out how much it moves every frame. Multiplying it by the framerate (60 in this case) will get us pixels/second.

### Find out the speed of the plane
```
self.last_x, self.last_y = self.pos

self.pos = (self.pos[0] + (self.xVel * self.dt), self.pos[1])

self.length_traveled = sqrt((self.pos[0] - self.last_x)**2 + (self.pos[1] - self.last_y)**2)
```
To get the speed of the plane or the enemy in this case, we just do the same Thing. Good thing this program is purely for demonstration, if not I would write some function to save on lines.
### Find out the needed offset to hit the plane
```
# When the target bullet is None it typically means that the gun hasn't shot any bullets yet, so we just set the bullet speed to some arbitrary value, making sure it's not 0 to prevent division with 0 later in the code.
if self.target_bullet != None:
	bullet_speed = self.target_bullet.get_speed()
else:
	bullet_speed = 1

distance = sqrt((self.pos[0] - self.enemy.pos[0])**2 + (self.pos[1] - self.enemy.pos[1])**2)

offset = ((distance / bullet_speed) * self.enemy.get_speed()) * self.enemy.xDir

enemy_position_x = self.enemy.pos[0] + self.enemy.rect.width // 2 * self.enemy.xDir

enemy_position_y = self.enemy.pos[1] + self.enemy.rect.height // 2

difference_x = enemy_position_x + offset - self.pos[0] 
difference_y = enemy_position_y - self.pos[1]

# Plug the difference into this function to get the radians
angle = atan2(difference_y, difference_x)
# Convert the radians into an angle and return it
angle = degrees(angle)
```
Here I've split up the code a bit to make it easier to read. But it's basically the same as the first time we figured out the angle between the enemy and the shooter. But you can also see that we used the position of the enemy to figure out the angle, so if we add in the offset we will aim ahead of the enemy. To find said offset we just divide the distance between the enemy and the shooter, with the speed of the bullet to get the time the bullet takes to travel between the enemy and the shooter. Then we multiply that time by the speed of the enemy, getting the distance the enemy has traveled in the time the bullet takes to travel between the shooter and the enemy.
## Conclusion
Although the steps done above aim the bullets toward the enemy with the right-ish offset, there are still some minor things we have to add for the bullets to hit accurately and that i didn't mention above:
- Add a variable to determine the direction of the enemy.

Due to us adding the offset to the position of the enemy, the shooter aims ahead of the enemy when it's going forward and continues to do so as the enemy travels backwards. To fix this we add the xDir variable, if we negate whatever xDir is every time the enemy changes direction, we can keep track of the direction of the enemy at all times. Then we just multiply the offset by xDir, which is either 1 or -1. Effectively changing to which side we want to aim ahead.
### Without xDir 
<img src="https://s4.gifyu.com/images/bruh1ce523c32fbafe203.gif" width="45%">

```
offset = ((distance / bullet_speed) * self.enemy.get_speed())
```

### With xDir
<img src="https://s4.gifyu.com/images/bruh15fafbbbbbe16aeb4.gif" width="45%">

```
offset = ((distance / bullet_speed) * self.enemy.get_speed()) * self.enemy.xDir
```
[See where this code is from](https://github.com/Acaippa/pygame-areal-fighters/edit/main/readme.md#find-out-the-needed-offset-to-hit-the-plane)

- Move the center of the enemy to the middle of enemy.

In pygame, the origin of the coordinate system in in the top left. Making the shooter aim for the top left corner of the enemy rather than the middle. Due to the slight inaccuracy of the shooter, it increases the chance of the bullet missing.

### Aiming at top left corner
<img src="https://s4.gifyu.com/images/bruh1b0e46c7c39fedaaf.gif" width="45%">

```
enemy_position_x = self.enemy.pos[0]
```
### Aiming at center
<img src="https://s4.gifyu.com/images/bruh19b9c165b9d55f168.gif" width="45%">

```
enemy_position_x = self.enemy.pos[0] + self.enemy.rect.width // 2 * self.enemy.xDir
```
[See where this code is from](https://github.com/Acaippa/pygame-areal-fighters/edit/main/readme.md#find-out-the-needed-offset-to-hit-the-plane)

Although the difference is very small, im thinking the satisfaction of the bullet hitting acurately makes up for it.
