import random, pygame, sys
from pygame.locals import *
from random import randint
import copy
import math
import time
import pickle
import os
#defining the window size and other different specifications of the window
FPS = 5
WINDOWWIDTH = 640
WINDOWHEIGHT = 640
boxsize = min(WINDOWWIDTH,WINDOWHEIGHT)//4;
margin = 5
thickness = 0
#defining the RGB for various colours used
WHITE= (255, 255, 255)
BLACK= (  0,   0,   0)
RED = (255,   0,   0)
GREEN= (  0, 255,   0)
DARKGREEN= (  0, 155,   0)
DARKGRAY= ( 40,  40,  40)
LIGHTSALMON=(255, 160, 122)
ORANGE=(221, 118, 7)
LIGHTORANGE=(227,155,78)
CORAL=(255, 127, 80)
BLUE = (0, 0, 255)
LIGHTBLUE = (0, 0, 150)
colorback=(189,174,158)
colorblank=(205,193,180)
colorlight=(249,246,242)
colordark=(119,110,101)

fontSize=[100,85,70,55,40]

dictcolor1={
0:colorblank,
2:(238,228,218),
4:(237,224,200),
8:(242,177,121),
16:(245,149,99),
32:(246,124,95),
64:(246,95,59),
128:(237,207,114),
256:(237,204,97),
512:(237,200,80),
1024:(237,197,63),
2048:(237,194,46),
4096:(237,190,30),
8192:(239,180,25) }

dictcolor2={
2:colordark,
4:colordark,
8:colorlight,
16:colorlight,
32:colorlight,
64:colorlight,
128:colorlight,
256:colorlight,
512:colorlight,
1024:colorlight,
2048:colorlight,
4096:colorlight,
8192:colorlight }
BGCOLOR = LIGHTORANGE
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

TABLE=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def matrix_to_tuple(matrix):
    return tuple(map(tuple, matrix))

def print_tuple_contents(tup):
    for row in tup:
        for element in row:
            print(element, end=" ")
        print()  # Print a newline after printing each row


# Example usage:
q_table = {}

# Check if the file exists
if os.path.exists('q_values.pkl'):
    # Load Q-values from the file
    with open('q_values.pkl', 'rb') as f:
        q_table = pickle.load(f)
    print('Q-values loaded from the file')
else:
    with open('q_values.pkl', 'wb') as f:
        pickle.dump(q_table, f)
    print('Initial Q-values saved to the file')


def main():
    global FPSCLOCK, screen, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('2048')

    showStartScreen()

    while True:
        runGame(TABLE)
        gameover()


def createButton(text, x, y, width, height, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+width > mouse[0] > x and y+height > mouse[1] > y:
        pygame.draw.rect(screen, LIGHTBLUE, (x,y,width,height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, BLUE, (x,y,width,height))

    smallText = pygame.font.Font('freesansbold.ttf',50)
    TextSurf = smallText.render(text,True,WHITE)
    TextRect = TextSurf.get_rect()
    TextRect.center = ((x+(width/2)),(y+(height/2)))
    screen.blit(TextSurf, TextRect)


def showStartScreen():
#the start screen
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('2048', True, WHITE, ORANGE)

    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT/8)
        screen.blit(display_rect, rectangle)

        createButton("NEW GAME", 80, 180, 480, 80, newGame)
        createButton("HIGHSCORE", 80, 340, 480, 80, leaderboard)
        createButton("QUIT", 80, 500, 480, 80, terminate)

        if checkForKeyPress():
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def newGame():
    runGame(TABLE)

def randomfill(TABLE):
    # search for zero in the game table and randomly fill the places
    flatTABLE = sum(TABLE,[])
    if 0 not in flatTABLE:
        return TABLE
    empty=False
    w=0
    while not empty:
        w=randint(0,15)
        if TABLE[w//4][w%4] == 0:
            empty=True
    z=randint(1,5)
    if z==5:
        TABLE[w//4][w%4] = 4
    else:
        TABLE[w//4][w%4] = 2
    return TABLE

def gameOver(TABLE):
    # returns False if a box is empty or two boxes can be merged
    x = [-1, 0, 1, 0 ]
    y = [0 , 1, 0, -1]
    for pi in range(4):
        for pj in range(4):
            if TABLE[pi][pj] ==8:
                return True
    return False

def showGameOverMessage():
# to show game over screen
    titleFont = pygame.font.Font('freesansbold.ttf', 60)
    titleSurf1 = titleFont.render('Game Over', True, WHITE, ORANGE)
    showMainMenu()
    #main()
    

    while True:
        screen.fill(BGCOLOR)
        display_rect = pygame.transform.rotate(titleSurf1, 0)
        rectangle = display_rect.get_rect()
        rectangle.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        screen.blit(display_rect, rectangle)

        showMainMenu()
        pygame.display.update()
        #main()
        if checkForKeyPress():
            if len(pygame.event.get()) > 0:
                main()
        FPSCLOCK.tick(FPS)

def showMainMenu():
# to display main menu
    pressKeySurf = BASICFONT.render('Press a key for main menu', True, WHITE)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 250, WINDOWHEIGHT - 30)
    screen.blit(pressKeySurf, pressKeyRect)

def checkForKeyPress():
    #checking if a key is pressed or not
    if len(pygame.event.get(QUIT)) > 0:
        with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(q_table, f)
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def show(TABLE):
    #showing the table
    screen.fill(colorback)
    myfont = pygame.font.SysFont("Arial", 60, bold=True)
    for i in range(4):
        for j in range(4):
            pygame.draw.rect(screen, dictcolor1[TABLE[i][j]], (j*boxsize+margin,
                                              i*boxsize+margin,
                                              boxsize-2*margin,
                                              boxsize-2*margin),
                                              thickness)
            if TABLE[i][j] != 0:
                order=int(math.log10(TABLE[i][j]))
                myfont = pygame.font.SysFont("Arial", fontSize[order] , bold=True)
                label = myfont.render("%4s" %(TABLE[i][j]), 1, dictcolor2[TABLE[i][j]] )
                screen.blit(label, (j*boxsize+2*margin, i*boxsize+9*margin))
                
    pygame.display.update()

def runGame(TABLE):
    TABLE=randomfill(TABLE)
    TABLE=randomfill(TABLE)
    show(TABLE)
    state = matrix_to_tuple(TABLE)

    action_with_highest_q_value = 0   #this is dummy action 
    
    # Check if the entry for the state is empty
    if state not in q_table:
        q_table[state] = {action: 0 for action in range(4)}
    else:
        # Get the action with the highest Q-value
        action_with_highest_q_value = max(q_table[state], key=q_table[state].get)

    running=True

    while True:
        # Check for quit event
        for event in pygame.event.get():
            if event.type == QUIT:
                print("quit")
                with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(q_table, f)
                pygame.quit()
                sys.exit()

        # Select action with the highest Q-value
        action_with_highest_q_value = max(q_table[state], key=q_table[state].get)

        # print("currstate: ")
        # for i in range(4):
        #     for j in range(4):
        #         print(TABLE[i][j], end=",")
        #     print("")
        # print("Q[currState] = {",q_table[state][0],",",q_table[state][1],",",q_table[state][2],",",q_table[state][3],"}")
        # Map action index to desired key
        if action_with_highest_q_value == 0:
            desired_key = "w"
            print("chosen up")
        elif action_with_highest_q_value == 1:
            desired_key = "s"
            print("chosen down")
        elif action_with_highest_q_value == 2:
            desired_key = "a"
            print("chosen left")
        elif action_with_highest_q_value == 3:
            desired_key = "d"
            print("chosen right")
        else:
            desired_key = None
        time.sleep(2)

        # Perform action
        if desired_key is not None:
            new_table = key(desired_key, copy.deepcopy(TABLE),action_with_highest_q_value,state)
            if new_table != TABLE:
                TABLE = randomfill(new_table)
                show(TABLE)

            if new_table == TABLE:
                q_table[state][action_with_highest_q_value] = q_table[state][action_with_highest_q_value] - 100000
   

            if gameOver(TABLE):
                # Show game over message or reset the game
                print("Game finished!")
                time.sleep(2)
                TABLE = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
                runGame(TABLE)

def key(DIRECTION,TABLE,action_with_highest_q_value,prevstate):
    if   DIRECTION =='w':
        for pi in range(1,4):
            for pj in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveup(pi,pj,TABLE,action_with_highest_q_value,prevstate)
    elif DIRECTION =='s':
        for pi in range(2,-1,-1):
            for pj in range(4):
                if TABLE[pi][pj] !=0: TABLE=movedown(pi,pj,TABLE,action_with_highest_q_value,prevstate)
    elif DIRECTION =='a':
        for pj in range(1,4):
            for pi in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveleft(pi,pj,TABLE,action_with_highest_q_value,prevstate)
    elif DIRECTION =='d':
        for pj in range(2,-1,-1):
            for pi in range(4):
                if TABLE[pi][pj] !=0: TABLE=moveright(pi,pj,TABLE,action_with_highest_q_value,prevstate)
    return TABLE

####################     FIX THIS
def tuples_equal(tuple1, tuple2):
    if len(tuple1) != len(tuple2):
        return False
    for i in range(len(tuple1)):
        if len(tuple1[i]) != len(tuple2[i]):
            return False
        for j in range(len(tuple1[i])):
            if tuple1[i][j] != tuple2[i][j]:
                return False
    return True



def movedown(pi,pj,T,action_with_highest_q_value,previous_state):
    justcomb=False
    reward=0
    while pi < 3 and (T[pi+1][pj] == 0 or (T[pi+1][pj] == T[pi][pj] and not justcomb)):
        if T[pi+1][pj] == 0:
            T[pi+1][pj] = T[pi][pj]    # punish little bit here
        elif T[pi+1][pj]==T[pi][pj]:
            T[pi+1][pj] += T[pi][pj]    # reward here
            reward = reward+T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pi+=1

    q_table[previous_state][action_with_highest_q_value] = q_table[previous_state][action_with_highest_q_value] + reward
    return T

def moveleft(pi,pj,T,action_with_highest_q_value,previous_state):
    justcomb=False
    reward=0
    while pj > 0  and (T[pi][pj-1] == 0 or (T[pi][pj-1] == T[pi][pj] and not justcomb)):
        if T[pi][pj-1] == 0:
            T[pi][pj-1] = T[pi][pj]   
        elif T[pi][pj-1]==T[pi][pj]:
            T[pi][pj-1] += T[pi][pj]
            reward = reward+T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pj-=1

    # if (previous_state == matrix_to_tuple(T)):
    #     print("same state found")
    #     reward = -100000
    q_table[previous_state][action_with_highest_q_value] = q_table[previous_state][action_with_highest_q_value] + reward
    return T

def moveright(pi,pj,T,action_with_highest_q_value,previous_state):
    justcomb=False
    reward=0
    while pj < 3 and (T[pi][pj+1] == 0 or (T[pi][pj+1] == T[pi][pj] and not justcomb)):
        if T[pi][pj+1] == 0:
            T[pi][pj+1] = T[pi][pj]
        elif T[pi][pj+1]==T[pi][pj]:
            T[pi][pj+1] += T[pi][pj]
            reward = reward+T[pi][pj]
            justcomb=True
        T[pi][pj] = 0
        pj+=1

    # if (previous_state == matrix_to_tuple(T)):
    #     print("same state found")
    #     reward = -100000
    q_table[previous_state][action_with_highest_q_value] = q_table[previous_state][action_with_highest_q_value] + reward
    
    return T

def moveup(pi,pj,T,action_with_highest_q_value,previous_state):
    justcomb=False
    reward=0
    while pi > 0 and (T[pi-1][pj] == 0 or (T[pi-1][pj] == T[pi][pj] and not justcomb)):
        if T[pi-1][pj] == 0:
            T[pi-1][pj] = T[pi][pj] 
        elif T[pi-1][pj]==T[pi][pj]:
            T[pi-1][pj] += T[pi][pj]
            reward = reward+T[pi][pj]
            justcomb=True
        T[pi][pj]=0
        pi-=1
    # print("previous state:")
    # print_tuple_contents(previous_state)
    # print("\nT:")
    # print_tuple_contents(matrix_to_tuple(T))
    # if tuples_equal(previous_state,matrix_to_tuple(T)):
    #     print("same state found")
    #     reward = -100000
    q_table[previous_state][action_with_highest_q_value] = q_table[previous_state][action_with_highest_q_value] + reward
    return T

def leaderboard():
    s = 'to show leaderboard'

def terminate():
    with open('q_values.pkl', 'wb') as f:
                    print("Saved Q-values to file")
                    pickle.dump(q_table, f)
    pygame.quit()
    sys.exit()

main()
