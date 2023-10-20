import os
import time
import random
from pytimedinput import timedKey

SCORE_UP = 50
ROW_LENGTH = 16
COLUMN_LENGTH = 16
CELL_COUNT = ROW_LENGTH*COLUMN_LENGTH
MAX_CELL = CELL_COUNT-1
MOVE_DIR = {
'n': -(ROW_LENGTH),
's': ROW_LENGTH,
'e': 1,
'w': -1}
TURN_LEFT = {
'n': 'w',
's': 'e',
'e': 'n',
'w': 's'}
TURN_RIGHT = {
'n': 'e',
's': 'w',
'e': 's',
'w': 'n'}

def clear_terminal():
    if(os.name == 'nt'):
        os.system('cls')
    else:
        os.system('clear')

def goal_set(player_pos, player_body):
    player_body.append(player_pos)
    goal = random.randint(0,MAX_CELL)
    while(goal in player_body):
        goal = random.randint(0,MAX_CELL)
    return goal

def move_player(player_pos, player_dir):
    new_pos = player_pos+MOVE_DIR[player_dir]
    if(player_dir == 'n' or player_dir == 's'):
        if(new_pos < 0):
            new_pos = new_pos+CELL_COUNT
        elif(new_pos > MAX_CELL):
            new_pos = new_pos-CELL_COUNT
    elif(new_pos%ROW_LENGTH == 0 and player_dir == 'e'):
        new_pos = new_pos-(ROW_LENGTH-1)
    elif(new_pos%ROW_LENGTH == ROW_LENGTH-1 and player_dir == 'w'):
        new_pos = new_pos+ROW_LENGTH
    return new_pos

def snake_shuffle(player_pos, player_body):
    n=len(player_body)
    to_move=player_pos
    while(n>0):
        n=n-1
        temp = player_body[n]
        player_body[n] = to_move
        to_move = temp
    return player_body

def proximity_check(player_pos, player_dir, player_body):
    forwards = move_player(player_pos, player_dir)
    left = move_player(player_pos, TURN_LEFT[player_dir])
    right = move_player(player_pos, TURN_RIGHT[player_dir])
    
    forwards_danger = (forwards in player_body)
    left_danger = (left in player_body)
    right_danger = (right in player_body)
    
    return (forwards_danger, left_danger, right_danger)

def draw_display(player_pos, player_dir, goal, score, dead, forwards_danger, left_danger, right_danger):
    clear_terminal()
    score_str = str(score+100000)[1:6]
    if(dead):
        print("You died!")
        print("Score: " + score_str)
    else:
        units_down = str(player_pos//ROW_LENGTH)
        units_right = str(player_pos%ROW_LENGTH)
        pos_str = units_down + "S" + units_right + "E"
        
        units_down = str(goal//ROW_LENGTH)
        units_right = str(goal%ROW_LENGTH)
        goal_str = units_down + "S" + units_right + "E"
        
        dir_str = "  " + player_dir.upper() + "  "
        
        forwards = "!!!^!!!" if forwards_danger else "   ^   "
        left = "!<!" if left_danger else " < "
        right = "!>!" if right_danger else " > "
        
        print(pos_str + "   " + forwards + "   " + goal_str)
        print(dir_str + "   " + left + " " + right + "   " + score_str)
        
        

def main():
    running = True
    player_pos = random.randint(0,MAX_CELL)
    player_dir = 'e'
    player_body = []
    goal = goal_set(player_pos, player_body)
    score = 0
    dead = False
    draw_display(player_pos, player_dir, goal, score, dead, False, False, False)
    while(running):
        time.sleep(0.2)
        turn_dir, time_up = timedKey("", timeout=0.8, resetOnInput=False, allowCharacters="ad")
        if(not time_up):
            if(turn_dir == 'a'):
                player_dir = TURN_LEFT[player_dir]
            elif(turn_dir == 'd'):
                player_dir = TURN_RIGHT[player_dir]
        
        new_pos = move_player(player_pos, player_dir)
        if(new_pos in player_body):
            dead = True
        if(new_pos == goal):
            player_body.append(player_pos)
            player_pos = new_pos
            goal = goal_set(player_pos, player_body)
            score = score+SCORE_UP
        else:
            player_body = snake_shuffle(player_pos, player_body)
            player_pos = new_pos
        
        proximity_alert = proximity_check(player_pos, player_dir, player_body)
        
        draw_display(player_pos, player_dir, goal, score, dead, proximity_alert[0], proximity_alert[1], proximity_alert[2])
            
        


if __name__ == "__main__":
    main()
