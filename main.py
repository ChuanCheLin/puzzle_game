from random import randint
import pygame
import os
from puzzle import Puzzle 
from preprocessing import cut_image_into_pieces
import cv2
# Settings
size = 4 # N x N puzzle
img = cv2.imread('puzzle/1.jpg')

# Window
WIDTH = 1200
HEIGHT = 600

# puzzle
start_x = 200
start_y = 20
puzzle_height, puzzle_width, channels = img.shape
height_unit, width_unit = cut_image_into_pieces(img, size)

# colors
white = (255, 255, 255)
black = (0, 0, 0)

def is_in_rectangle(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx+rw) and (ry <= y <= ry+rh):
        return True
    return False

def draw_puzzle_frame():
    screen.fill(white)    
    pygame.draw.rect(screen, black, (start_x - 1, start_y - 1, puzzle_width, puzzle_height))
    pygame.draw.rect(screen, white, (start_x, start_y, puzzle_width -2 ,puzzle_height-2))
    pygame.draw.rect(screen, black, (2, 2, 40, 40))
    
# draw every puzzle pieces    
def draw_puzzle_pieces():
    for i in range(len(puzzles)):
        current_puzzle = puzzles[len(puzzles)-i-1]
        screen.blit(current_puzzle.img, current_puzzle.pos)

# redraw the frame and puzzle pieces        
def redraw_all():
    if current_puzzle.is_move:
        # redraw the frame
        draw_puzzle_frame()
                                
        x, y = event.pos
        # start point
        image_w, image_h = current_puzzle.img.get_size()
        # destination point
        new_image_x = x - image_w/2
        new_image_y = y - image_h/2
        
        current_puzzle.pos = [new_image_x, new_image_y]
        
        for j in current_puzzle.group:
            if j == i or puzzles[j].lock == True:
                continue
            else:
                w = current_puzzle.axis[0] - puzzles[j].axis[0]
                h = current_puzzle.axis[1] - puzzles[j].axis[1]
                puzzles[j].pos = [new_image_x - w*width_unit, new_image_y - h*height_unit]
                
        # redraw every puzzle pieces
        draw_puzzle_pieces()
        pygame.display.update()
    

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('puzzle game')
    draw_puzzle_frame()
    
    puzzles = []
    moveable = True # make sure that only one puzzle is moveable
    
    for i in range(size*size):
        #load puzzle pieces
        current_image = pygame.image.load(os.path.join("temp", f"{i}.png")).convert_alpha()
        # initial position (random)
        image_x = randint (0, WIDTH - 200)
        image_y = randint (0, HEIGHT - 200)
        axis = [i % size, i // size]
        
        puzzles.append(Puzzle(current_image, [image_x, image_y], [start_x + (i % size)*(width_unit), start_y + (i//size)*(height_unit)], axis, i))
    draw_puzzle_pieces()
    pygame.display.flip()
    
    # build neighbors
    for i in range(len(puzzles)):
        
        current_puzzle = puzzles[i]
        #left
        if (i - 1) >= 0 and i % size != 0:
            current_puzzle.left = puzzles[i - 1]
        #right
        if (i + 1) < len(puzzles) and (i+1) % size != 0:
            current_puzzle.right = puzzles[i + 1]
        #top
        if (i - size) >= 0 :
            current_puzzle.top = puzzles[i - size]
        #bottom
        if (i + size) < len(puzzles):
            current_puzzle.bottom = puzzles[i + size]
            
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            
            # check click on which puzzle pieces
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                for i in range(len(puzzles)):
                    current_puzzle = puzzles[i]
                    w, h = current_puzzle.img.get_size()
                    pos = current_puzzle.pos
                    if is_in_rectangle(event.pos, (pos[0], pos[1], w, h)) and moveable == True and current_puzzle.lock == False:
                        current_puzzle.is_move = True
                        moveable = False
            # cancel the selection on the puzzle piece       
            if event.type == pygame.MOUSEBUTTONUP:
                for i in range(len(puzzles)):
                    current_puzzle = puzzles[i]
                    if current_puzzle.check_neighbors(height_unit, width_unit, puzzles):
                        redraw_all()
                    current_puzzle.check_boundary()
                    
                    # reset
                    current_puzzle.is_move = False
                    moveable = True
    
                    draw_puzzle_frame()
                    draw_puzzle_pieces()
                    pygame.display.update()
                    #print(current_puzzle.group)
                    
            # move the seclected puzzle piece    
            if event.type == pygame.MOUSEMOTION:
                
                for i in range(len(puzzles)):
                    current_puzzle = puzzles[i]
                    redraw_all()