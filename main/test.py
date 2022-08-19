import pygame


pygame.init()
screen = pygame.display.set_mode((500, 400))
clock = pygame.time.Clock()


class Bullet:
    # provide an argument for what to check and what to exclude
    def __init__(self, start_pos, x_direction, check, exclude):
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=start_pos)
        self.x_direction = x_direction
        self.check, self.exclude = check, exclude
        self.x_velocity = 5 * self.x_direction
        self.damage = 5
        self.destroy = False

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def update(self):
        # go over the list of entities to check
        for entity in self.check:
            # if the entity is not the one that is excluded and the entity has
            # attributes that are needed here check for collision
            # and if there is then set the destroy flag to True
            # and stop updating. Also some check to see if the bullet has traveled
            # too far or somethin like that could be added
            if (entity is not self.exclude and hasattr(entity, 'health')
                    and hasattr(entity, 'rect')):
                if self.rect.colliderect(entity.rect):
                    entity.health -= self.damage
                    self.destroy = True
                    return
        self.rect.move_ip(self.x_velocity, 0)


# simple entity class to represent entities (in this case
# only the players and enemies since theoretically this could
# be base class both for bullets and players and enemies)
class Entity:
    def __init__(self, x, y, color, name):
        self.color, self.name = color, name
        self.rect = pygame.Rect(x, y, 30, 60)
        self.health = 100
        self.prev_health = self.health

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def update(self):
        # if health has been reduced print the current health
        if self.health < self.prev_health:
            print(f'{self.name} health: {self.health}')
            self.prev_health = self.health


# create the entities
player = Entity(100, 200, (0, 255, 0), 'player')
enemy = Entity(370, 200, (255, 0, 0), 'enemy')
# create a list to store bullets in
bullets = []

while True:
    screen.fill((0, 0, 0))
    
    # create a list for bullets to remove
    # so that they can be removed later
    # without interfering with the checking for loop
    remove_bullets = []
    for bullet in bullets:
        # if the bullet should be destroyed don't update it
        # and add to the bullets to remove
        if bullet.destroy:
            remove_bullets.append(bullet)
        else:
            bullet.update()
            bullet.draw(screen)
    # remove destroyed bullets from the main list
    for bullet in remove_bullets:
        bullets.remove(bullet)
    
    # update
    enemy.update()
    enemy.draw(screen)

    player.update()
    player.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            # usually you would just pass a list of entities that are not like
            # this but rather referenced by name so you would use that
            # instead of passing a list like this. In that case it would make more
            # sense to have an excluded entity as in this case you could just not include
            # in the list at all. Also going over a list to remove a single element
            # would likely be more wasteful
            if event.key == pygame.K_a:
                # if a pressed create a bullet traveling from enemy to player
                bullet = Bullet(enemy.rect.center, -1, [player, enemy], enemy)
                bullets.append(bullet)
            if event.key == pygame.K_d:
                # if d pressed create a bullet traveling from player to enemy
                bullet = Bullet(player.rect.center, 17, [player, enemy], player)
                bullets.append(bullet)

    pygame.display.update()
    clock.tick(60)