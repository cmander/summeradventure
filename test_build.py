import pygame
from pygame.locals import *
import sys
import time
import pyganim

class Camera(object):
    def checkLocation(self):
        # Checking player position to determine camera scrolling

        # Left scrolling condition
        if p1.xPos < WIDTHCENTER - 50:
            p1.xPos = WIDTHCENTER - 50
            if p1.moveRight == False and p1.moveLeft == True:
                self.x_scroll = True
                self.y_scroll = False
                self.update(self.x_scroll, self.y_scroll, 5, 0)

        # Right scrolling condition
        elif p1.xPos + p1.playerWidth > WIDTHCENTER + 50:
            p1.xPos = (WIDTHCENTER + 50) - p1.playerWidth
            if p1.moveRight == True and p1.moveLeft == False:
                self.x_scroll = True
                self.y_scroll = False
                self.update(self.x_scroll, self.y_scroll, -5, 0)

        # Up scrolling condition
        elif p1.yPos < HEIGHTCENTER - 50:
            p1.yPos = HEIGHTCENTER - 50
            if p1.moveUp == True and p1.moveDown == False:
                self.x_scroll = False
                self.y_scroll = True
                self.update(self.x_scroll, self.y_scroll, 0, 5)

        # Down scrolling condition
        elif p1.yPos + p1.playerHeight > HEIGHTCENTER + 50:
            p1.yPos = (HEIGHTCENTER + 50) - p1.playerHeight
            if p1.moveUp == False and p1.moveDown == True:
                self.x_scroll = False
                self.y_scroll = True
                self.update(self.x_scroll, self.y_scroll, 0, -5)

    def update(self, x_scroll, y_scroll, x_rate, y_rate):
        for e in levelOne.entities_list:
            if x_scroll == False and y_scroll == True:
                e.rect.top += y_rate
            if x_scroll == True and y_scroll == False:
                e.rect.left += x_rate

class Level:
    def __init__(self):
        self.block_list = []
        self.entities_list = []
        self.blit_list = []

        self.isMid = True
        self.isTop = False
        self.isLeft = False
        self.isRight = False

    def clearLists(self):
        pass

    def blitImages(self):
        [windowSurface.blit(b.image, b.rect) for b in self.blit_list]

class Player(pygame.sprite.Sprite):
    def __init__(self):
        
        self.xPos = 300
        self.yPos = 200

        self.front_standing = pygame.image.load('ness_frames/ness_walkdown00.gif')
        self.back_standing = pygame.image.load('ness_frames/ness_walkup00.gif')
        self.left_standing = pygame.image.load('ness_frames/ness_walkleft00.gif')
        self.right_standing = pygame.image.load('ness_frames/ness_walkright00.gif')
        self.down_left_standing = pygame.image.load('ness_frames/ness_walkdownleft00.gif')
        self.up_left_standing = pygame.image.load('ness_frames/ness_walkupleft00.gif')

        self.playerWidth, self.playerHeight = self.front_standing.get_size()

        self.animTypes = 'walkdown walkup walkleft walkdownleft walkupleft'.split()
        self.animObjs = {}
        for animType in self.animTypes:
            self.imagesAndDurations = [('ness_frames/ness_%s%s.gif' % (animType, str(num).rjust(2, '0')), 0.1) for num in range(2)]
            self.animObjs[animType] = pyganim.PygAnimation(self.imagesAndDurations)

        # create right-facing sprites
        self.animObjs['walkright'] = self.animObjs['walkleft'].getCopy()
        self.animObjs['walkright'].flip(True, False)
        self.animObjs['walkright'].makeTransformsPermanent()
        self.animObjs['walkdownright'] = self.animObjs['walkdownleft'].getCopy()
        self.animObjs['walkdownright'].flip(True, False)
        self.animObjs['walkdownright'].makeTransformsPermanent()
        self.animObjs['walkupright'] = self.animObjs['walkupleft'].getCopy()
        self.animObjs['walkupright'].flip(True, False)
        self.animObjs['walkupright'].makeTransformsPermanent()

        self.direction = DOWN # starting direction        

        self.moveUp = self.moveDown = self.moveLeft = self.moveRight = False
        self.upPressed = self.downPressed = self.leftPressed = self.rightPressed = False

    def move(self):
        for event in pygame.event.get(): # event handling loop

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    self.upPressed = True
                    self.moveUp = True
                    self.moveDown = False
                    if not self.moveLeft and not self.moveRight:
                        self.direction = UP
                elif event.key == K_DOWN:
                    self.downPressed = True
                    self.moveUp = False
                    self.moveDown = True
                    if not self.moveLeft and not self.moveRight:
                        self.direction = DOWN
                elif event.key == K_LEFT:
                    self.leftPressed = True
                    self.moveLeft = True
                    self.moveRight = False
                    if not self.moveUp and not self.moveDown:
                        self.direction = LEFT
                elif event.key == K_RIGHT:
                    self.rightPressed = True
                    self.moveLeft = False
                    self.moveRight = True
                    if not self.moveUp and not self.moveDown:
                        self.direction = RIGHT                      

            elif event.type == KEYUP:
                if event.key == K_UP:
                    self.upPressed = False
                    self.moveUp = False
                    if self.moveLeft:
                        self.direction = LEFT
                    if self.moveRight:
                        self.direction = RIGHT
                elif event.key == K_DOWN:
                    self.downPressed = False
                    self.moveDown = False
                    if self.moveLeft:
                        self.direction = LEFT
                    if self.moveRight:
                        self.direction = RIGHT
                elif event.key == K_LEFT:
                    self.leftPressed = False
                    self.moveLeft = False
                    if self.moveUp:
                        self.direction = UP
                    if self.moveDown:
                        self.direction = DOWN
                elif event.key == K_RIGHT:
                    self.rightPressed = False
                    self.moveRight = False
                    if self.moveUp:
                        self.direction = UP
                    if self.moveDown:
                        self.direction = DOWN

        # Walk cycle and camera scroll method calling

        if self.moveUp or self.moveDown or self.moveLeft or self.moveRight:
            moveConductor.play()
            if self.direction == UP:
                self.moveDown = self.moveLeft = self.moveRight = False
                camera.checkLocation()
                self.animObjs['walkup'].blit(windowSurface, (self.xPos, self.yPos))
            elif self.direction == DOWN:
                self.moveUp = self.moveLeft = self.moveRight = False
                camera.checkLocation()
                self.animObjs['walkdown'].blit(windowSurface, (self.xPos, self.yPos))
            elif self.direction == LEFT:
                self.moveUp = self.moveDown = self.moveRight = False
                camera.checkLocation()
                self.animObjs['walkleft'].blit(windowSurface, (self.xPos, self.yPos))
            elif self.direction == RIGHT:
                self.moveUp = self.moveDown = self.moveLeft = False
                camera.checkLocation()
                self.animObjs['walkright'].blit(windowSurface, (self.xPos, self.yPos))           

            # move player

            if self.moveUp:
                self.yPos -= WALKRATE
            if self.moveDown:
                self.yPos += WALKRATE
            if self.moveLeft:
                self.xPos -= WALKRATE
            if self.moveRight:
                self.xPos += WALKRATE

        else:
            # standing still
            moveConductor.stop()
            if self.direction == UP:
                windowSurface.blit(self.back_standing, (self.xPos, self.yPos))                   
            elif self.direction == DOWN:
                windowSurface.blit(self.front_standing, (self.xPos, self.yPos))
            elif self.direction == LEFT:
                windowSurface.blit(self.left_standing, (self.xPos, self.yPos))
            elif self.direction == RIGHT:
                windowSurface.blit(self.right_standing, (self.xPos, self.yPos))            

        # screen boundary interaction
        if self.xPos < 0:
            self.xPos = 0
        if self.xPos > WINDOWWIDTH - self.playerWidth:
            self.xPos = WINDOWWIDTH - self.playerWidth
        if self.yPos < 0:
            self.yPos = 0
        if self.yPos > WINDOWHEIGHT - self.playerHeight:
            self.yPos = WINDOWHEIGHT - self.playerHeight

class Background(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, image):        
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.width, self.height = self.image.get_size()
        self.rect.left = xPos
        self.rect.top = yPos   

    def draw(self):
        windowSurface.blit(self.image, self.rect)

    def blockPlayer(self, player):
        if player.yPos < self.rect.top:            
            levelTop()
        elif player.yPos > self.rect.bottom - player.playerHeight:            
            player.yPos = self.rect.bottom - player.playerHeight
        elif player.xPos < self.rect.left:
            player.xPos = self.rect.left
        elif player.xPos > self.rect.right - player.playerWidth:
            player.xPos = self.rect.right - player.playerWidth

class Block(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, image):     
        
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.left = xPos
        self.rect.top = yPos
        self.block_list = []

    def drawBlock(self):
        self.block_list.append(self)
        for b in block_list:
            windowSurface.blit(b.image, b.rect)

    def blockPlayer(self, player):
        if player.yPos + player.playerHeight > self.rect.top and player.yPos < self.rect.bottom:
            if player.xPos < self.rect.right and player.xPos + player.playerWidth > self.rect.right:
                player.xPos = self.rect.right
            if player.xPos > self.rect.left - player.playerWidth and player.xPos < (self.rect.left - player.playerWidth) + 10:
                player.xPos = self.rect.left - player.playerWidth
        if player.xPos + player.playerWidth > self.rect.left and player.xPos < self.rect.right:
            if player.yPos < self.rect.bottom and player.yPos + player.playerHeight > self.rect.bottom - 10:
                player.yPos = self.rect.bottom
            if player.yPos > self.rect.top - player.playerHeight and player.yPos < (self.rect.top - player.playerHeight) + 10:
                player.yPos = self.rect.top - player.playerHeight



def levelTop():
    levelOne.isTop = True
    levelOne.isLeft = levelOne.isRight = levelOne.isMid = False

    [levelOne.block_list.remove(b) for b in levelOne.block_list]
    [levelOne.entities_list.remove(e) for e in levelOne.entities_list]
    [levelOne.blit_list.remove(b) for b in levelOne.blit_list]    

    b1 = Block(200, 150, 'tree.gif')
    b2 = Block(300, 50, 'tree.gif')

    levelOne.block_list = [b1, b2]
    levelOne.entities_list = [land, b1, b2]
    [levelOne.blit_list.append(e) for e in levelOne.entities_list]

    [b.drawBlock() for b in levelOne.block_list]

    #land.blockPlayer(p1)
    [b.blockPlayer(p1) for b in levelOne.block_list]

    levelOne.blitImages()

    land.rect.bottom = p1.yPos + p1.playerHeight

def levelMid():
    levelOne.isMid = True
    levelOne.isLeft = levelOne.isRight = levelOne.isTop = False
    
    # setting up mid section of level
    levelOne.block_list = [b1, b2, b3]
    levelOne.entities_list = [land, b1, b2, b3]
    [levelOne.blit_list.append(e) for e in entities_list]
        
    sea.draw()   

    [b.drawBlock() for b in levelOne.block_list]
        
    land.blockPlayer(p1)
    [b.blockPlayer(p1) for b in levelOne.block_list]

    levelOne.blitImages()

    

def main():
    gameIsPlaying = True

    while gameIsPlaying:

        sea.draw()

        if levelOne.isMid == True:
            levelMid()
        elif levelOne.isTop == True:
            levelTop()
        elif levelOne.isLeft == True:
            pass
        

        levelMid()

        p1.move()

        pygame.display.update()
        windowSurface.fill(WHITE)
        mainClock.tick(30)

        [levelOne.block_list.remove(b) for b in levelOne.block_list]
        [levelOne.entities_list.remove(e) for e in levelOne.entities_list]
        [levelOne.blit_list.remove(b) for b in levelOne.blit_list]

    


        
pygame.init()

# All constant variables

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
UPLEFT = 'up left'
DOWNLEFT = 'down left'
UPRIGHT = 'up right'
DOWNRIGHT = 'down right'

WHITE = (255, 255, 255)
BGCOLOUR = WHITE

WALKRATE = 3 # Player velocity.

LEVELWIDTH = 1000
LEVELHEIGHT = 1000

WINDOWWIDTH = 640
WINDOWHEIGHT = 480
WIDTHCENTER = WINDOWWIDTH / 2
HEIGHTCENTER = WINDOWHEIGHT / 2


windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)
pygame.display.set_caption('Summer Adventure Test')
mainClock = pygame.time.Clock()

levelOne = Level()

p1 = Player()

sea = Background(0, 0, 'sea.gif')
land = Background(50, 50, 'land.gif')

b1 = Block(100, 200, 'tree.gif')
b2 = Block(300, 350, 'tree.gif')
b3 = Block(350, 100, 'tree.gif')


camera = Camera()

blit_list = []
block_list = [b1, b2, b3]
entities_list = [land, b1, b2, b3]

moveConductor = pyganim.PygConductor(p1.animObjs)

main()
