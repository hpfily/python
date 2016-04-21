#-*- coding:utf-8 -*-
import pygame
from gameobjects.vector2 import Vector2
from pygame.locals import *
from sys import exit
from os  import getcwd
print "hello world"

class Role_Sprit(pygame.sprite.Sprite):    
    def __init__(self,surface,row,col):
        pygame.sprite.Sprite.__init__ (self)
        self.row    = row
        self.col    = col
        self.surface= surface
        self.allrect= self.getrect(surface,row,col)
        self.rect   = ()
        self.frame  = 0
        self._rate  = 100       # 100ms every frame 10pfs.
        self.passed_time = 0

    def getrect(self,surface,row=None,col=None):
        self.height  = surface.get_height()/row
        self.width   = surface.get_width()/col
        if row == None:
            return surface
        directionlist = ['DownLeft','UpLeft','DownRight','UpRight']
        rect    = { }
        temp    = [ ]
        for y in xrange(row):
            for x in xrange(col):
                temp.append(Rect((x*self.width,y*self.height),(self.width,self.height)))
                if x== (col-1):
                    rect[directionlist[y]]=temp
                    temp = [] 
        print   rect
        return  rect

    def update(self,direction,passed_time):
        assert(self.allrect.has_key(direction))
        self.direction   = direction
        #print self.direction
        self.passed_time += passed_time
        self.frame  = (self.passed_time/self._rate)%self.col
        if self.frame == 0 and self.passed_time > self._rate:
            self.passed_time = 0
        self.rects  = self.allrect[self.direction]
        self.rect   = self.rects[self.frame]


class Role(object):
    def __init__(self,staysprit,runsprit):
        self.staysprit  = staysprit
        self.runsprit   = runsprit
        self.sprit      = staysprit
#        self.surface    = surface
        self.location   = Vector2(400,300)
        self.destination= Vector2(0,0)
        self.direction  = 'DownLeft'
        self.state      = 'stay'
        self.speed      = 200  #
    def render(self,screen):
        if self.state == 'stay':
            self.sprit  = self.staysprit
        else:
            self.sprit  = self.runsprit
        x,y=self.location
        screen.blit(self.sprit.surface,(x-self.sprit.width/2,y-self.sprit.height/2),self.sprit.rect)

    def process(self,destination,passed_time):
        self.destination   = destination
        self.vec           = self.destination - self.location
        #print self.vec
        self.vec_len       = self.vec.get_length()
        if self.vec_len > 10:
            self.state     = 'run'
            self.vec_eye   = self.vec.get_normalized()

            if self.vec[0] >0:
                if self.vec[1] >0:
                    self.direction = 'DownRight'
                elif self.vec[1]<0:
                    self.direction = 'UpRight'
            elif self.vec[0]<0:
                if self.vec[1] >0:
                    self.direction = 'DownLeft'
                elif self.vec[1]<0:
                    self.direction = 'UpLeft'
                    
            self.location = self.location+ self.vec_eye*self.speed*passed_time/1000
            self.runsprit.update(self.direction,passed_time)
        else:
            self.state    = 'stay'
            self.staysprit.update(self.direction,passed_time)
            
                            
pygame.init()

screen  = pygame.display.set_mode((800,600),0,32)
pygame.display.set_caption("hello world!")
homedir = getcwd()
print homedir
bg = pygame.image.load(homedir+'/pic/bg.jpg').convert()
spritSurface=pygame.image.load(homedir+'/pic/sprit.png').convert_alpha()
#getrect(spritSurface,4,8)
spritRunSurface=pygame.image.load(homedir+'/pic/sprit_run.png').convert_alpha()
stay =  Role_Sprit(spritSurface,4,8)
run  =  Role_Sprit(spritRunSurface,4,8)
role =  Role(stay,run)


#RED=(255,0,0)
#ll.set_colorkey(RED)
clock= pygame.time.Clock()
pos=role.location
while True:
    for event in pygame.event.get():
        if event.type ==QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            print event.pos
            pos=event.pos
    time = clock.tick()
#    stay.update('UpLeft',time)
#    run.update('UpLeft',time)
    screen.blit(bg,(0,0))
    role.process(pos,time)
    role.render(screen)
#    screen.blit(stay.surface,(300,300),stay.rect)
#    screen.blit(run.surface,(400,300),run.rect)


    pygame.display.update()
#    raw_input()
#    clock.tick(10)
#    pygame.display.set_caption("fps:"+str(clock.get_fps()))
    
    
