import pandas as pd
import copy
import random

# team (byg)
# conference (bg)
# division (bg)
# position (byg)
# height (arrow) (byg)
# age (arrow) (byg)
# jersey (arrow) (byg)

west_teams = {'northwest':['DEN','MIN','OKC','UTA','POR'],'pacific':['SAC','PHX','LAC','LAC','GSW'],'southwest':['MEM','DAL','SAS','HOU','NOP']}
east_teams = {'atlantic':['BOS','PHI','NYK','BKN','TOR'],'central':['MIL','CLE','IND','CHI','DET'],'southeast':['MIA','ATL','WAS','ORL','CHA']}

df = pd.read_csv('nba_player_info_updated.csv',index_col=False)
remaining_players = df['Player'].unique().tolist()

remaining_teams = []
remaining_positions = ['G','G-F','F-G','F','F-C','C-F','C']
correct_height = [x for x in range(70,87)]
correct_jersey = [x for x in range(0,100)]
prev_position_guesses = []

def get_initial_guess():
    global remaining_teams
    global remaining_positions
    global correct_height
    global correct_jersey
    global prev_position_guesses
    global west_teams
    global east_teams
    initial_guess = input('Who was your first guess? ').split(' ',1)
    initial_guess = ''.join(initial_guess)
    initial_guess_info = df.loc[df['Player'] == initial_guess]
    prev_position_guesses.append(initial_guess_info['Position'].values[0])
    df.drop(df.loc[df['Player']==initial_guess].index, inplace=True) 

    initial_guess_team = input('What color was TEAM (b, y, or g)? ')
    initial_guess_conf = input('What color was CONF (b or g)? ')
    initial_guess_div = input('What color was DIV (b or g)? ')
    if initial_guess_team == 'g':
        remaining_teams = [initial_guess_info['Team'].values[0]]
    elif initial_guess_conf == 'b' and initial_guess_div == 'b':
        if any(initial_guess_info['Team'].values[0] in div for div in west_teams.values()):
            for teams in east_teams.values():
                remaining_teams += teams 
        else:
            for teams in west_teams.values():
                remaining_teams += teams
    elif initial_guess_conf == 'g':
        if initial_guess_div == 'b':
            if any(initial_guess_info['Team'].values[0] in div for div in west_teams.values()):
                remaining_west_teams = copy.deepcopy(west_teams)
                for div in west_teams:
                    if initial_guess_info['Team'].values[0] in west_teams[div]:
                        del remaining_west_teams[div]
                for teams in remaining_west_teams.values():
                    remaining_teams += teams 
            else:
                remaining_east_teams = copy.deepcopy(east_teams)
                for div in east_teams:
                    if initial_guess_info['Team'].values[0] in east_teams[div]:
                        del remaining_east_teams[div]
                for teams in remaining_east_teams.values():
                    remaining_teams += teams 
        elif initial_guess_div == 'g':
            if any(initial_guess_info['Team'].values[0] in div for div in west_teams.values()):
                for div in west_teams:
                    if initial_guess_info['Team'].values[0] in west_teams[div]:   
                        remaining_teams = west_teams[div]
                        remaining_teams.remove(initial_guess_info['Team'].unique().tolist()[0])
            else:
                for div in east_teams:
                    if initial_guess_info['Team'].values[0] in east_teams[div]:
                        remaining_teams = east_teams[div]
                        remaining_teams.remove(initial_guess_info['Team'].unique().tolist()[0])

    initial_guess_pos = input('What color was POS (b, y, or g)? ')
    if initial_guess_pos == 'g':
        remaining_positions = [initial_guess_info['Position'].values[0]]
    elif initial_guess_pos == 'y':
        if initial_guess_info['Position'].values[0] == 'G':
            remaining_positions = remaining_positions[1:3]
        elif initial_guess_info['Position'].values[0] == 'G-F' or 'F-G':
            remaining_positions = remaining_positions[0:6]
            remaining_positions.remove(initial_guess_info['Position'].values[0])
        elif initial_guess_info['Position'].values[0] == 'F':
            remaining_positions = remaining_positions[1:6]
            remaining_positions.remove(initial_guess_info['Position'].values[0])  
        elif initial_guess_info['Position'].values[0] == 'F-C' or 'C-F':
            remaining_positions = remaining_positions[1:7]
            remaining_positions.remove(initial_guess_info['Position'].values[0])
        elif initial_guess_info['Position'].values[0] == 'C':
            remaining_positions = remaining_positions[4:6]
    elif initial_guess_pos == 'b':
        if initial_guess_info['Position'].values[0] == 'G':
            remaining_positions = remaining_positions[3:]
        elif initial_guess_info['Position'].values[0] == 'G-F' or 'F-G':
            remaining_positions = remaining_positions[5:]
        elif initial_guess_info['Position'].values[0] == 'F':
            remaining_positions = ['G','C']
        elif initial_guess_info['Position'].values[0] == 'F-C' or 'C-F':
            remaining_positions = remaining_positions[:2]
        elif initial_guess_info['Position'].values[0] == 'C':
            remaining_positions = remaining_positions[0:4]       

    initial_guess_height = input('What color was HT (b, y, or g)? ')
    initial_guess_height_range = [x for x in range(initial_guess_info['Height'].values[0]-2,initial_guess_info['Height'].values[0]+3)]
    if initial_guess_height == 'b':
        correct_height = [height for height in correct_height if height not in initial_guess_height_range]
    elif initial_guess_height == 'y':
        correct_height = initial_guess_height_range
    elif initial_guess_height == 'g':
        correct_height = [initial_guess_info['Height'].values[0]]
    
    initial_guess_age = input('What color was AGE (b, y, or g)? ')

    initial_guess_jersey = input('What color was # (b, y, or g)? ')   
    initial_guess_jersey_range = [x for x in range(initial_guess_info['Number'].values[0]-2,initial_guess_info['Number'].values[0]+3)]
    if initial_guess_jersey == 'b':
        correct_jersey = [jersey for jersey in correct_jersey if jersey not in initial_guess_jersey_range]
    elif initial_guess_jersey == 'y':
        correct_jersey = initial_guess_jersey_range
    elif initial_guess_jersey == 'g':
        correct_jersey = [initial_guess_info['Number'].values[0]]

    remove_unfitting_players()

def get_subsequent_guess():
    global remaining_teams
    global remaining_positions
    global correct_height
    global correct_jersey
    global prev_position_guesses
    global west_teams
    global east_teams
    subsequent_guess = input('Who was your next guess? ').split(' ',1)
    subsequent_guess = ''.join(subsequent_guess)
    subsequent_guess_info = df.loc[df['Player'] == subsequent_guess]
    prev_position_guesses.append(subsequent_guess_info['Position'].values[0])
    df.drop(df.loc[df['Player']==subsequent_guess].index, inplace=True) 

    subsequent_guess_team = input('What color was TEAM (b, y, or g)? ')
    subsequent_guess_conf = input('What color was CONF (b or g)? ')
    subsequent_guess_div = input('What color was DIV (b or g)? ')
    if subsequent_guess_team == 'g':
        remaining_teams = [subsequent_guess_info['Team'].values[0]]
    elif subsequent_guess_conf == 'g':
        if subsequent_guess_div == 'b':
            if any(subsequent_guess_info['Team'].values[0] in div for div in west_teams.values()):
                for div in west_teams:
                    if subsequent_guess_info['Team'].values[0] in west_teams[div]:
                        remaining_teams = [team for team in remaining_teams if team not in west_teams[div]]
            else:
                for div in east_teams:
                    if subsequent_guess_info['Team'].values[0] in east_teams[div]:
                        remaining_teams = [team for team in remaining_teams if team not in east_teams[div]]
        elif subsequent_guess_div == 'g':
            if any(subsequent_guess_info['Team'].values[0] in div for div in west_teams.values()):
                for div in west_teams:
                    if subsequent_guess_info['Team'].values[0] in west_teams[div]:   
                        remaining_teams.remove(subsequent_guess_info['Team'].unique().tolist()[0])
            else:
                for div in east_teams:
                    if subsequent_guess_info['Team'].values[0] in east_teams[div]:   
                        remaining_teams.remove(subsequent_guess_info['Team'].unique().tolist()[0])

    subsequent_guess_pos = input('What color was POS (b, y, or g)? ')
    if subsequent_guess_pos == 'g':
        remaining_positions = [subsequent_guess_info['Position'].values[0]]
    elif subsequent_guess_pos == 'y':
        if subsequent_guess_info['Position'].values[0] == 'G':
            remaining_positions = [pos for pos in remaining_positions[1:3] if pos not in prev_position_guesses]         
        elif subsequent_guess_info['Position'].values[0] == 'G-F' or 'F-G':
            remaining_positions = [pos for pos in remaining_positions[0:6] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'F':
            remaining_positions = [pos for pos in remaining_positions[1:6] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'F-C' or 'C-F':
            remaining_positions = [pos for pos in remaining_positions[1:7] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'C':
            remaining_positions = [pos for pos in remaining_positions[4:6] if pos not in prev_position_guesses]
        if subsequent_guess_info['Position'].values[0] in remaining_positions: 
            remaining_positions.remove(subsequent_guess_info['Position'].values[0])    
    elif subsequent_guess_pos == 'b':
        if subsequent_guess_info['Position'].values[0] == 'G':
            remaining_positions = [pos for pos in remaining_positions[3:] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'G-F' or 'F-G':
            remaining_positions = [pos for pos in remaining_positions[5:] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'F':
            remaining_positions = [pos for pos in ['G','C'] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'F-C' or 'C-F':
            remaining_positions = [pos for pos in remaining_positions[:2] if pos not in prev_position_guesses]
        elif subsequent_guess_info['Position'].values[0] == 'C':
            remaining_positions = [pos for pos in remaining_positions[0:4] if pos not in prev_position_guesses]
        if subsequent_guess_info['Position'].values[0] in remaining_positions: 
            remaining_positions.remove(subsequent_guess_info['Position'].values[0])     

    subsequent_guess_height = input('What color was HT (b, y, or g)? ')
    subsequent_guess_height_range = [x for x in range(subsequent_guess_info['Height'].values[0]-2,subsequent_guess_info['Height'].values[0]+3)]
    if subsequent_guess_height == 'b':
        correct_height = [height for height in correct_height if height not in subsequent_guess_height_range]
    elif subsequent_guess_height == 'y':
        correct_height = subsequent_guess_height_range
    elif subsequent_guess_height == 'g':
        correct_height = [subsequent_guess_info['Height'].values[0]]
    
    subsequent_guess_age = input('What color was AGE (b, y, or g)? ')

    subsequent_guess_jersey = input('What color was # (b, y, or g)? ')   
    subsequent_guess_jersey_range = [x for x in range(subsequent_guess_info['Number'].values[0]-2,subsequent_guess_info['Number'].values[0]+3)]
    if subsequent_guess_jersey == 'b':
        correct_jersey = [jersey for jersey in correct_jersey if jersey not in subsequent_guess_jersey_range]
    elif subsequent_guess_jersey == 'y':
        correct_jersey = subsequent_guess_jersey_range
    elif subsequent_guess_jersey == 'g':
        correct_jersey = [subsequent_guess_info['Number'].values[0]]
    
    remove_unfitting_players()

def remove_unfitting_players():
    global df
    global remaining_players
    df = df[df['Team'].isin(remaining_teams)]
    df = df[df['Number'].isin(correct_jersey)]
    df = df[df['Position'].isin(remaining_positions)]
    df = df[df['Height'].isin(correct_height)]
    remaining_players = df['Player'].unique().tolist()

get_initial_guess()
for num in range (0,7):
    is_guess_correct = input('Was that right (y or n)? ')
    if is_guess_correct != 'y':
        print('The remaining players are: \n',remaining_players)
        print('You should guess ' + random.choice(remaining_players) + ' next!')
        get_subsequent_guess()
        num += 1
    else:
        print('Yay!')
        break
