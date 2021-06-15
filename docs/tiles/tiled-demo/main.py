import pygame, pytmx

#Background color
BACKGROUND = (20, 20, 20)
RED = (255, 0, 0)

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 480

#Tiled map layer of tiles that you collide with
MAP_COLLISION_LAYER = 1

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Pygame Tiled Demo")

class Text:
    def __init__(self, text, pos=(0, 0)):
        self.font = pygame.font.Font(None, 24)
        self.color = (255, 255, 255)
        self.text = text
        self.pos = pos
        self.render(text)

    def render(self, text):
        self.image = self.font.render(text, 1, self.color)

    def draw(self):
        screen.blit(self.image, self.pos)


class Game:
    # Create a Game class
    def __init__(self):
        #Set up a level to load
        self.currentLevelNumber = 0
        self.levels = []
        self.levels.append(Level(fileName = "resources/level1.tmx"))
        self.currentLevel = self.levels[self.currentLevelNumber]
        
        #Create a player object and set the level it is in
        self.player = Player(200, 100)
        self.player.currentLevel = self.currentLevel
        
        #Draw aesthetic overlay
        self.overlay = pygame.image.load("resources/overlay.png")
        self.clock = pygame.time.Clock()
        self.running = True
        self.debugging = False
        self.text = Text('game')
        self.text_fps = Text('fps', (0, 24))
        self.rect = pygame.Rect(10, 10, 100, 100)
        print(self)
        
    def __str__(self):
        return f'{self.__class__.__name__} levels:{len(self.levels)}'
        
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.debugging = not self.debugging
                        print(f'debug: {self.debugging}')
                    elif event.key == pygame.K_t:
                        #print('resolution:', pygame.TIMER_RESOLUTION)
                        print('ticks:', pygame.time.get_ticks())
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.key.get_mods() & 256:
                        self.player.rect.center = event.pos
                    else:
                        self.rect.topleft = event.pos
                        group = self.currentLevel.layers[MAP_COLLISION_LAYER].tiles
                        hits = pygame.sprite.spritecollide(self, group, False)
                        for hit in hits:
                            print(hit.__class__.__name__, hit.rect)

                self.player.do_event(event)

            self.text.render(f'ticks:{pygame.time.get_ticks()}')
            self.text_fps.render(f'fps:{self.clock.get_fps():.2f}')

            self.player.update()
            self.draw(screen)
            self.clock.tick(60)

        pygame.quit()
    
    #Draw level, player, overlay
    def draw(self, screen):
        screen.fill(BACKGROUND)
        self.currentLevel.draw(screen)
        self.player.draw(screen)
        if self.debugging:
            screen.blit(self.overlay, [100, 100])

        self.text.draw()
        self.text_fps.draw()
        pygame.draw.rect(screen, RED, self.rect, 1)
        pygame.display.flip()
        
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        #Load the spritesheet of frames for this player
        self.sprites = SpriteSheet("resources/player.png", (30, 42))
    
        self.stillRight = self.sprites.image_at(0, 0)
        self.stillLeft = self.sprites.image_at(0, 1)
        
        #List of frames for each animation
        self.runningRight = [self.sprites.image_at(i, 2) for i in range(5)]
        self.runningLeft =  [self.sprites.image_at(i, 3) for i in range(5)]
        self.jumpingRight = [self.sprites.image_at(i, 0) for i in (1, 2, 3)]
        self.jumpingLeft  = [self.sprites.image_at(i, 1) for i in (1, 2, 3)]

        self.image = self.stillRight
        
        #Set player position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        #Set speed and direction
        self.changeX = 0
        self.changeY = 0
        self.direction = "right"
        
        #Boolean to check if player is running, current running frame, and time since last frame change
        self.running = False
        self.runningFrame = 0
        self.runningTime = pygame.time.get_ticks()
        
        #Players current level, set after object initialized in game constructor
        self.currentLevel = None

    def __str__(self):
        return f'Player at {self.rect.center} dir:{self.direction}'

    def do_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.direction = "left"
                self.running = True
                self.changeX = -3
            elif event.key == pygame.K_RIGHT:
                self.direction = "right"
                self.running = True
                self.changeX = 3
            elif event.key == pygame.K_UP:
                self.jump()
            elif event.key == pygame.K_SPACE:
                print(self)
            
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.changeX < 0:
                self.running = False
                self.changeX = 0
            elif event.key == pygame.K_RIGHT and self.changeX > 0:
                self.running = False
                self.changeX = 0
        
    def update(self):
        #Update player position by change
        self.rect.x += self.changeX
        
        #Get tiles in collision layer that player is now touching
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        if len(tileHitList) > 0:
            print(tileHitList)
        
        #Move player to correct side of that block
        for tile in tileHitList:
            if self.changeX > 0:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right
        
        #Move screen if player reaches screen bounds
        if self.rect.right >= SCREEN_WIDTH - 200:
            difference = self.rect.right - (SCREEN_WIDTH - 200)
            self.rect.right = SCREEN_WIDTH - 200
            self.currentLevel.shiftLevel(-difference)
        
        #Move screen is player reaches screen bounds
        if self.rect.left <= 200:
            difference = 200 - self.rect.left
            self.rect.left = 200
            self.currentLevel.shiftLevel(difference)
        
        #Update player position by change
        self.rect.y += self.changeY
        
        #Get tiles in collision layer that player is now touching
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
       
        #If there are tiles in that list
        if len(tileHitList) > 0:
            #Move player to correct side of that tile, update player frame
            for tile in tileHitList:
                if self.changeY > 0:
                    self.rect.bottom = tile.rect.top
                    self.changeY = 1
                    
                    if self.direction == "right":
                        self.image = self.stillRight
                    else:
                        self.image = self.stillLeft
                else:
                    self.rect.top = tile.rect.bottom
                    self.changeY = 0
        #If there are not tiles in that list
        else:
            #Update player change for jumping/falling and player frame
            self.changeY += 0.2
            if self.changeY > 0:
                if self.direction == "right":
                    self.image = self.jumpingRight[1]
                else:
                    self.image = self.jumpingLeft[1]
        
        #If player is on ground and running, update running animation
        if self.running and self.changeY == 1:
            if self.direction == "right":
                self.image = self.runningRight[self.runningFrame]
            else:
                self.image = self.runningLeft[self.runningFrame]
        
        #When correct amount of time has passed, go to next frame
        if pygame.time.get_ticks() - self.runningTime > 50:
            self.runningTime = pygame.time.get_ticks()
            if self.runningFrame == 4:
                self.runningFrame = 0
            else:
                self.runningFrame += 1

    def animate(self):
        t = pygame.time.get_ticks()
        if t - self.t0 > 50:
            self.t0 = t
            self.runningFrame = (self.runningFrame + 1) % 4

            if self.running and self.changeY == 1:
                if self.direction == "right":
                    self.image = self.runningRight[self.runningFrame]
                else:
                    self.image = self.runningLeft[self.runningFrame]

    #Make player jump
    def jump(self):
        #Check if player is on ground
        self.rect.y += 2
        tileHitList = pygame.sprite.spritecollide(self, self.currentLevel.layers[MAP_COLLISION_LAYER].tiles, False)
        self.rect.y -= 2
        
        if len(tileHitList) > 0:
            if self.direction == "right":
                self.image = self.jumpingRight[0]
            else:
                self.image = self.jumpingLeft[0]
                
            self.changeY = -6
    
    #Draw player
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
class Level:
    def __init__(self, fileName):
        #Create map object from PyTMX
        self.file = fileName
        self.mapObject = pytmx.load_pygame(fileName)
        
        #Create list of layers for map
        self.layers = []
        
        #Amount of level shift left/right
        self.levelShift = 0
        
        #Create layers for each layer in tile map
        for layer in range(len(self.mapObject.layers)):
            self.layers.append(Layer(index = layer, mapObject = self.mapObject))
        print(self)
    
    #Move layer left/right
    def shiftLevel(self, shiftX):
        self.levelShift += shiftX
        
        for layer in self.layers:
            for tile in layer.tiles:
                tile.rect.x += shiftX
    
    #Update layer
    def draw(self, screen):
        for layer in self.layers:
            layer.draw(screen)

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file}'
            
class Layer:
    def __init__(self, index, mapObject):
        #Layer index from tiled map
        self.index = index
        
        #Create gruop of tiles for this layer
        self.tiles = pygame.sprite.Group()
        
        #Reference map object
        self.mapObject = mapObject
        
        #Create tiles in the right position for each layer
        for x in range(self.mapObject.width):
            for y in range(self.mapObject.height):
                img = self.mapObject.get_tile_image(x, y, self.index)
                if img:
                    tile = Tile(img, x * self.mapObject.tilewidth, y * self.mapObject.tileheight)
                    self.tiles.add(tile)
        print(self)

    #Draw layer
    def draw(self, screen):
        self.tiles.draw(screen)

    def __str__(self):
        return f'{self.__class__.__name__} index:{self.index} tiles:{len(self.tiles)}'

#Tile class with an image, x and y
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return f'{self.__class__.__name__} {self.rect}'

#Sprit sheet class to load sprites from player spritesheet
class SpriteSheet:
    def __init__(self, file_name, tile_size):
        self.file_name = file_name
        self.tile_size = tile_size
        self.sheet = pygame.image.load(file_name)
        self.rect = self.sheet.get_rect()
        print(self)

    def image_at(self, x, y):
        w, h = self.tile_size
        pos = w * x, h * y
        image = pygame.Surface(self.tile_size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), (pos, self.tile_size))
        return image

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file_name} size:{self.rect.size} tile:{self.tile_size}'

game = Game()
game.run()
