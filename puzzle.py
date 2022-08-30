import pygame
import os

thres = 6 # how much gap between true pos can be accectable

pygame.mixer.init()
# load music
lock_sound = pygame.mixer.Sound(os.path.join("sounds", "lock.mp3"))
between_sound = pygame.mixer.Sound(os.path.join("sounds", "between.mp3"))

class Puzzle():
    def __init__(self, img, pos, true_pos, axis, num):
        self.img = img
        self.pos = pos # [x, y]
        self.true_pos = true_pos # corresponding to outer frame
        
        self.group = set() # stick together
        self.group.add(num)
        self.num = num
        self.axis = axis
        self.is_move = False
        self.lock = False # lock == true => in the true position(true_pos)
        
        self.left = None
        self.right = None
        self.top = None
        self.bottom = None
        
    def check_neighbors(self, height_unit, width_unit, puzzles):
        x = self.pos[0]
        y = self.pos[1]
        det = False           
        
        #check left & top
        if self.left != None:    
            if (abs(x - width_unit - self.left.pos[0]) < thres and abs(y - self.left.pos[1]) < thres):
                if self.left.num not in self.group:
                    between_sound.play()
                    det = True
                self.group = set.union(self.left.group, self.group)
                self.left.group = self.group 
                
                for i in self.group:
                    puzzles[i].group = self.group
                
                
        if self.top != None:                    
            if (abs(x - self.top.pos[0]) < thres and abs(y - height_unit - self.top.pos[1]) < thres):
                if self.top.num not in self.group:
                    between_sound.play()
                    det = True
                self.group = set.union(self.top.group, self.group)
                self.top.group = self.group 
                
                for i in self.group:
                    puzzles[i].group = self.group
        return det        
                
    def check_boundary(self):
        x = self.pos[0]
        y = self.pos[1] 
        if self.lock == False:
            if (abs(x - self.true_pos[0]) < thres and abs(y - self.true_pos[1]) < thres):
                self.lock = True
                self.pos = self.true_pos
                lock_sound.play()