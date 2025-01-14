from turtle import color
# from django.shortcuts import redirect
import pygame as pg
from abaloneboard import Board
import math
import random
import Colors
from Values import state_value
from Node import Node
import sys
from button import Button
import time
import pygame
import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
from tkinter import colorchooser
from datetime import datetime
clock = pygame.time.Clock()
import numpy as np
import heapq




pg.init()
#clock = pygame.time.Clock()
LEVEL = "EASY" #default
LEVEL_BOOL = False
COLOR = 1
Human_turn = True #white will play first
Ai_turn = False

width = 1240
height = 720

# the game window screen
SCREEN = pygame.display.set_mode((width, height))

pygame.display.set_caption("PLay Abalone")

background_color = "#E8C491" # RGB values for white
SCREEN.fill(background_color)
pygame.display.update()

def get_font(size): # Returns font in the desired size
    return pygame.font.Font("PassionOne-Regular.ttf", size)

number_of_moves = 0
white_score = 0
black_score = 0
start_ticks = pygame.time.get_ticks()



import random

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, crossover_rate, generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.generations = generations

    def initial_population(self):
        # Generate an initial population of random strategies
        return [self.random_strategy() for _ in range(self.population_size)]

    def random_strategy(self):
        # Create a random strategy (e.g., sequence of moves or board configurations)
        strategy = [random.choice(['move1', 'move2', 'move3', 'move4']) for _ in range(10)]  # Example strategy
        return strategy

    def fitness(self, strategy, board):
        # Evaluate the fitness of a strategy
        # Fitness could be based on how many points the AI wins, how well it controls the board, etc.
        score = 0
        # Apply the strategy to the board and calculate the score
        # Example: score += board.evaluate(strategy)
        return score

    def selection(self, population, board):
        # Select the best strategies (parents) based on their fitness
        fitness_scores = [(self.fitness(strategy, board), strategy) for strategy in population]
        fitness_scores.sort(reverse=True)  # Sort by fitness
        selected = [strategy for score, strategy in fitness_scores[:self.population_size // 2]]  # Select top half
        return selected

    def crossover(self, parent1, parent2):
        # Perform crossover between two parents to create offspring
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
        else:
            child1, child2 = parent1, parent2  # No crossover, children are copies of parents
        return child1, child2

    def mutate(self, strategy):
        # Apply mutation to a strategy
        if random.random() < self.mutation_rate:
            point = random.randint(0, len(strategy) - 1)
            strategy[point] = random.choice(['move1', 'move2', 'move3', 'move4'])  # Example mutation
        return strategy

    def evolve(self, board):
        # Run the genetic algorithm to evolve strategies
        population = self.initial_population()

        for generation in range(self.generations):
            print(f"Generation {generation + 1}")
            selected = self.selection(population, board)
            next_generation = []

            # Generate next generation through crossover and mutation
            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)
                child1, child2 = self.crossover(parent1, parent2)
                next_generation.extend([self.mutate(child1), self.mutate(child2)])

            population = next_generation

        # Return the best strategy from the final population
        best_strategy = self.selection(population, board)[0]
        return best_strategy
# Parameters: population size, mutation rate, crossover rate, generations
ga = GeneticAlgorithm(population_size=20, mutation_rate=0.1, crossover_rate=0.7, generations=50)
if not Human_turn:
    print("Genetic Algorithm is evolving the best strategy...")
    # Assume `board` is the current state of the game board
    best_strategy = ga.evolve(board)  # Evolve the best strategy using GA
    print(f"Best strategy found: {best_strategy}")

    # Apply the best move from the evolved strategy
    new_move = best_strategy[0]  # For example, the first move in the strategy
    board.make_move(new_move)  # Assuming make_move accepts a strategy move
    Human_turn = True
def fitness(self, strategy, board):
    score = 0
    # Example: Apply each move in the strategy to a copy of the board and evaluate the final state
    for move in strategy:
        board_copy = board.copy()
        board_copy.apply_move(move)
        score += board_copy.evaluate()
    return score


if not Human_turn:
    print("Genetic Algorithm is evolving the best strategy...")
    
    # Assume `board` is the current state of the game board
    best_strategy = ga.evolve(board)  # Evolve the best strategy using GA
    print(f"Best strategy found: {best_strategy}")

    # Apply the best move from the evolved strategy
    new_move = best_strategy[0]  # For example, the first move in the strategy
    board.make_move(new_move)  # Assuming make_move accepts a strategy move
    Human_turn = True





class AStar:
    def __init__(self, start, goal, board):
        self.start = start
        self.goal = goal
        self.board = board

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        result = []
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < len(self.board) and 0 <= neighbor[1] < len(self.board[0]) and self.board[neighbor[0]][neighbor[1]] != 2:
                result.append(neighbor)
        return result

    def a_star_search(self):
        print("A* search started from:", self.start, "to", self.goal)
        open_set = []
        heapq.heappush(open_set, (0, self.start))
        came_from = {}
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.goal)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if current == self.goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.neighbors(current):
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path


if not Human_turn:
    root.nodestate = board.boardState  # Update root before playing the move
    root.children = []

    # Example positions, replace these with actual positions you need in your game
    start_position = (start_x, start_y)
    goal_position = (goal_x, goal_y)

    astar = AStar(start_position, goal_position, root.nodestate)
    best_path = astar.a_star_search()

    if best_path:
        new_move = best_path[1]  # Select the next move on the path
        board.make_move(new_move)
        Human_turn = True


def time_membership(crisp_second):
    degree = {}
    degree['very_early'] = 0
    degree['early'] = 0
    degree['ok'] = 0
    degree['late'] = 0
    degree['very_late'] = 0
    if 0<=crisp_second<15:
        degree['very_early'] = 1
    elif 15<=crisp_second<20:
        degree['very_early'] = (20-crisp_second)/(20-15)
        degree['early'] = (crisp_second-15)/(25-15)
    elif 20<=crisp_second<25:
        degree['early'] = (crisp_second-15)/(25-15)
    elif 25<=crisp_second<27:
        degree['early'] = (30-crisp_second)/(30-25)
    elif 27<=crisp_second<30:
        degree['early'] = (30-crisp_second)/(30-25)
        degree['ok'] = (crisp_second-27)/(34-27)
    elif 30<=crisp_second<34:
        degree['ok'] = (crisp_second-27)/(34-27)
    elif 34<=crisp_second<40:
        degree['ok'] = (40-crisp_second)/(40-34)
        degree['late'] = (crisp_second-34)/(45-34)
    elif 40<=crisp_second<45:
        degree['late'] = (crisp_second-34)/(45-34)
    elif 45<=crisp_second<55:
        degree['late'] = 1
    elif 55<=crisp_second<65:
        degree['late'] = (65-crisp_second)/(65-55)
        degree['very_late'] = (crisp_second-55)/(65-55)
    elif crisp_second>=65:
        degree['very_late'] = 1
    
    return degree
         

def t_n_m_membership(n):
    degree = {}
    degree['low'] = 0
    degree['avg'] = 0
    degree['huge'] = 0
    if 0<=n<7:
        degree['low'] = 1
    elif 7<=n<10:
        degree['low'] = (10-n)/(10-7)
        degree['avg'] = (n-7)/(10-7)
    elif 10<=n<11:
        degree['avg'] = (12-n)/(12-10)
    elif 11<=n<12:
        degree['avg'] = (12-n)/(12-10)
        degree['huge'] = (n-11)/(13-11)
    elif 12<=n<13:
        degree['huge'] = (n-11)/(13-11)
    elif n>=13:
        degree['huge'] = 1
    
    return degree

def piece_membership(n):
    degree = {}
    degree['poor'] = 0
    degree['good'] = 0
    degree['best'] = 0

    if 0<=n<3:
        degree['poor'] = 1
    elif 3<=n<5:
        degree['poor'] = (5-n)/(5-3)
        degree['good'] = (n-3)/(5-3)
    elif 5<=n<7:
        degree['good'] = (7-n)/(7-5)
        degree['best'] = (n-5)/(7-5)
    elif n>=7:
        degree['best'] = 1

    return degree

def evaluate_black_player_rating(sec_degree, M_degree, W_degree, B_degree):
    rating = {
        'worst': 0,
        'bad': 0,
        'moderate': 0,
        'good': 0,
        'excellent': 0
    }
    rating['excellent'] = max(
                        min(
                            min( max(B_degree['good'],B_degree['best']),max(W_degree['good'],W_degree['poor'])),max(max(sec_degree['very_early'],sec_degree['early']), max(M_degree['avg'],M_degree['low']))
                            ),
                        min(
                            min( B_degree['best'],max(W_degree['good'],W_degree['poor'])),max(max(sec_degree['ok'],sec_degree['early']), max(M_degree['avg'],M_degree['low']))
                            )
                        )
    
    rating['good'] = max(
                        min(
                            min( max(B_degree['good'],B_degree['best']),max(W_degree['good'],W_degree['poor'])),max(max(sec_degree['ok'],sec_degree['late']), max(M_degree['huge'],M_degree['avg']))
                            ),
                        min(
                            min( max(B_degree['good'],B_degree['best']),max(W_degree['good'],W_degree['poor'])),max(max(sec_degree['ok'],sec_degree['early']), max(M_degree['avg'],M_degree['low']))
                            )
                        )
    
    rating['moderate'] = max(
                            min(
                                min(max(B_degree['poor'],B_degree['good']),max(W_degree['best'],W_degree['good'])),min(max(sec_degree['late'],sec_degree['ok']), M_degree['huge'])
                                ),
                            min(
                                min(max(B_degree['poor'],B_degree['good']),max(W_degree['best'],W_degree['good'])),min(max(sec_degree['early'],sec_degree['ok']), M_degree['avg'])
                                )
                            )
    
    rating['bad'] =  max( 
                        max(
                            min(
                                max(B_degree['poor'],max(W_degree['best'],W_degree['good'])),max(sec_degree['late'], M_degree['huge'])
                                ),
                            min(
                                max(B_degree['poor'],max(W_degree['best'],W_degree['good'])),max(sec_degree['ok'], M_degree['huge'])
                                )
                            ),
                        max(
                            min(
                                max(B_degree['poor'], max(W_degree['best'],W_degree['good'])), max(sec_degree['late'], M_degree['avg'])
                               ),
                            min(
                                max(B_degree['poor'], max(W_degree['best'],W_degree['good'])), max(sec_degree['ok'], M_degree['avg'])
                                )
                            )
                        )
    
    rating['worst'] = max( 
                        max(
                            min(
                                max(B_degree['poor'], W_degree['best']),max(sec_degree['very_late'], M_degree['huge'])
                                ),
                            min(
                                max(B_degree['poor'], W_degree['best']),max(sec_degree['late'], M_degree['huge'])
                                )
                            ),
                        max(
                            min(
                                max(B_degree['poor'], W_degree['best']), max(sec_degree['very_late'], M_degree['avg'])
                               ),
                            min(
                                max(B_degree['poor'], W_degree['best']), max(sec_degree['late'], M_degree['avg'])
                                )
                            )
                        )   


    return rating


def find_fuzzy_score(white_score,black_score,number_of_moves, elapsed_time):
    score = 0
    crisp_second = (elapsed_time - start_ticks) // 1000  # Get elapsed time in seconds
    print(crisp_second)
    sec_degree = time_membership(crisp_second)
    print(sec_degree)
    M_degree = t_n_m_membership(number_of_moves)
    print(M_degree)
    W_degree = piece_membership(white_score)
    print(white_score)
    print(W_degree)
    B_degree = piece_membership(black_score)
    print(black_score)
    print(B_degree)
    ratings_detail = evaluate_black_player_rating(sec_degree, M_degree, W_degree, B_degree)
    print(ratings_detail)
    values_list = np.array(list(ratings_detail.values())) * 100
    try:
        score  = ((values_list[0] * 40) + (values_list[1] * 50) + (values_list[2] * 60) + (values_list[3] * 70) + (values_list[4] * 80))/values_list.sum()
    except Exception as e:
        score = 0.6*100
    return score


def display_end_game_message(white_score,black_score,number_of_moves, elapsed_time):
    fuzzy_score = find_fuzzy_score(white_score,black_score,number_of_moves, elapsed_time)
    message = " AI Intelligence is "
    message += str(fuzzy_score)
    print(message)

    OPTIONS_TEXT = get_font(35).render(message, True, Colors.BLACK)
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(600, 225))
    SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
    
    pygame.display.update()
    pygame.time.delay(10000)  # Show the message for 3 seconds
 # Show the message for 3 seconds


def ok(SOLO = False):

    global LEVEL, LEVEL_BOOL,COLOR, Human_turn, number_of_moves,white_score,black_score

    MAX, MIN = 10000, -10000

    size = (1240, 720)
    # size = (900, 900)
    

    board_center = (int(size[0]/2), int(size[1]/2))
    # board_center = (int(size[0]/2 ), int(size[1]/2))

    print("BOARD CENTER : ", board_center)

    # ball_r = 32
    #ball radius
    ball_r = 22

    gap = ball_r//2
    dims = [ball_r, gap]
    board_length = 11*ball_r + 6*gap  # distance from centre to vertices
    current_ball = 0
    

    print("BALL_RADIUS : ", ball_r)
    print("GAP : ", gap)
    print("DIMENSIONS : ", dims)
    print("BOARD LENGTH : ", board_length)

    screen = pg.display.set_mode(size)
    screen.fill(background_color)
    pg.display.set_caption("Abalone")
    
    AI_TEXT = get_font(60).render("AI:", True, Colors.LOGO)
    AI_RECT = AI_TEXT.get_rect(center=(1100, 150))
    
    screen.blit(AI_TEXT,AI_RECT)
    YOU_TEXT = get_font(60).render("YOU:", True, Colors.LOGO)
    YOU_RECT = YOU_TEXT.get_rect(center=(1240-1100, 150))
    
    screen.blit(YOU_TEXT,YOU_RECT)
    QUIT = Button(image=None, pos=(1240-1100, 450), 
                        text_input="BACK", font=get_font(50), base_color=Colors.button, hovering_color="#760101")
   
    NEW_GAME = Button(image=None, pos=(1240-1100, 550), 
                        text_input="NEW GAME", font=get_font(50), base_color=Colors.button, hovering_color="#760101")
    
    clock = pg.time.Clock()
    running = True
    board = Board(board_center, board_length, screen, dims)
    board.initialize()
    root = Node(board.boardState, [], 0, []) # nodestate, move, value, children
    
    
    
    if(COLOR==1):  # if Black is set 
        board.draw(current_ball, Colors.BLACK, Colors.WHITE)
    else:
        board.draw(current_ball, Colors.WHITE,Colors.BLACK)

    pg.display.flip()
    while running:
        
        pygame.display.flip()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        # print(OPTIONS_MOUSE_POS)
    
        for button in [QUIT, NEW_GAME]:
           button.changeColor(OPTIONS_MOUSE_POS)
           button.update(SCREEN)
           
            
        
       
            
           
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                 if QUIT.checkForInput(OPTIONS_MOUSE_POS):
                     main_menu()

            if Human_turn:
               
                  if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos # to get the co ordinate at which mouse is clicked
                    #print(mouse_pos)
                    for i in range(9):
                        for j in range(len(board.grid[i])):
                            if board.grid[i][j].collidepoint(mouse_pos): # check if the clicked position is a valid co ordinate
                                if current_ball == 0 and board.boardState[i+1][j+1] == 1: #if no ball is selcted and the ball belongs to Human 
                                    current_ball = [i, j] # Then current ball is now holdng that position
                                    #print("CURRENT BALL VALUE : ", current_ball)
                                    break
                                elif [i,j]==current_ball:
                                    current_ball=0 # ball selection undo
                                    break
                                elif board.boardState[i+1][j+1]!=2 and current_ball!=0: # when some ball is already selected and another position is clicked to make a move , then the move is checked to be valid or not.
                                    #print(i,j)
                                    result = board.check_move(current_ball, [i, j])
                                    
                                    if result[0]:
                                        board.make_move(result[2]) # Do the move and update if any point achieved
                                        Human_turn = False
                                        current_ball = 0
                                        number_of_moves+=2
                                        
                                        break
                                else:
                                    print("YOU CAN'T MOVE WHITE")
            
            if not Human_turn:
                
                root.nodestate = board.boardState #updated root before playing the move
                root.children = []
               
                
                if(LEVEL=="EASY"):
                    new_move = board.minimax(3, root, True, float('-inf'),float('inf')).move
                else:
                    new_move = board.minimax(5, root, True, float('-inf'),float('inf')).move
                board.turn_counter += 1 # tracking no of turns
                board.make_move(new_move)
                
                Human_turn = True
                
                
            
            
            if(COLOR==1):  # if Black is set 
               board.draw(current_ball, Colors.BLACK, Colors.WHITE)
            else:
               board.draw(current_ball, Colors.WHITE,Colors.BLACK)
           #board.generate_moves(board.boardState, 2)
            
            if board.deleted == 1 or board.deleted == 2:
                board.deleted = 0
            if board.scoreAI == 6:
                white_score=board.scoreHum
                black_score=board.scoreAI
                elapsed_time = pygame.time.get_ticks()
                print('OOPS!You Lost')
                OPTIONS_TEXT = get_font(35).render("AI WON!!!", True, Colors.WHITE)
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(1200, 450))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
                # ended = True
                display_end_game_message(white_score,black_score,number_of_moves, elapsed_time)
                running = False
            if board.scoreHum == 6:
                white_score=board.scoreHum
                black_score=board.scoreAI
                elapsed_time = pygame.time.get_ticks()
                print('Hurrah!YOU WON!')
                OPTIONS_TEXT = get_font(35).render("YOU WON!!!", True, Colors.WHITE)
                OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(1200, 450))
                SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
                # ended = True
                display_end_game_message(white_score,black_score,number_of_moves, elapsed_time)
                running = False
           
            #board.generate_moves(board.boardState, 2)
            pg.display.flip()

            #clock.tick(60)
            
   

                   



def options():
    global LEVEL, LEVEL_BOOL, color_1, color_2, color_3, color_4, color_5,COLOR, Human_turn
    #
    LEVEL="EASY"
    COLOR=1 #default white represented by 1
    SCREEN.fill(background_color)
    pygame.display.set_caption("Setings")
    running = True
    while running:
        
        pygame.display.flip()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        #print(OPTIONS_MOUSE_POS)
        MENU_TEXT = get_font(80).render("SETTINGS", True, Colors.LOGO)
        MENU_RECT = MENU_TEXT.get_rect(center=(620, 120))
      
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        MODE_TEXT = get_font(80).render("MODE:", True, Colors.LOGO)
        MODE_RECT = MODE_TEXT.get_rect(center=(280, 260))
        SCREEN.blit(MODE_TEXT, MODE_RECT)
        
        COLOR_TEXT = get_font(80).render("SIDE:", True, Colors.LOGO)
        COLOR_RECT = COLOR_TEXT.get_rect(center=(280, 360))
        SCREEN.blit(COLOR_TEXT, COLOR_RECT)
       
        color2 = Colors.button
        BACK = Button(image=None, pos=(620, 500), 
                            text_input="BACK", font=get_font(80), base_color=Colors.button, hovering_color="#760101")
        
        #box = pygame.image.load("box.png")
        #box=pygame.transform.scale(box, (450,250))
        
        if LEVEL == "EASY":
           
           
            LEVEL_EASY = Button(image=None, pos=(480, 260), 
                                text_input="EASY", font=get_font(70), base_color="white", hovering_color="white")
            pygame.draw.rect(SCREEN,color2, LEVEL_EASY.rect)
            LEVEL_HARD = Button(image=None, pos=(700, 260), 
                                text_input="HARD", font=get_font(70), base_color=color2, hovering_color=Colors.hovering_color) 
            pygame.draw.rect(SCREEN, background_color, LEVEL_HARD.rect)
            
            LEVEL_EASY.update(SCREEN)
            LEVEL_HARD.update(SCREEN) 
        else:
            
            LEVEL_HARD = Button(image=None, pos=(700, 260), 
                                text_input="HARD", font=get_font(70),base_color="white",hovering_color="white" ) 
            
            pygame.draw.rect(SCREEN,color2, LEVEL_HARD.text_rect)
            LEVEL_EASY = Button(image=None, pos=(480, 260), 
                                text_input="EASY", font=get_font(70),base_color=color2, hovering_color=Colors.hovering_color)
            
            pygame.draw.rect(SCREEN, background_color, LEVEL_EASY.rect)
            
            LEVEL_EASY.update(SCREEN)
            LEVEL_HARD.update(SCREEN)
        if COLOR == 1:
            
            WHITE= Button(image=None, pos=(480, 360), 
                                text_input="WHITE", font=get_font(70), base_color="white", hovering_color="white")
            pygame.draw.rect(SCREEN,color2, WHITE.rect)
            BLACK = Button(image=None, pos=(700, 360), 
                                text_input="BLACK", font=get_font(70), base_color=color2, hovering_color=Colors.hovering_color) 
            pygame.draw.rect(SCREEN, background_color, BLACK.rect)
            WHITE.update(SCREEN)
            BLACK.update(SCREEN) 
        else:
            
            BLACK = Button(image=None, pos=(700, 360), 
                                text_input="BLACK", font=get_font(70),base_color="white",hovering_color="white" ) 
            pygame.draw.rect(SCREEN, color2, BLACK.rect)
            WHITE = Button(image=None, pos=(480, 360), 
                                text_input="WHITE", font=get_font(70),base_color=color2, hovering_color=Colors.hovering_color)
            pygame.draw.rect(SCREEN, background_color, WHITE.rect)
            BLACK.update(SCREEN)
            WHITE.update(SCREEN)
       
        for button in [LEVEL_EASY, LEVEL_HARD,BLACK,WHITE,BACK]:
           button.changeColor(OPTIONS_MOUSE_POS)
           button.update(SCREEN)
           
            
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
              
           
                if LEVEL_EASY.checkForInput(OPTIONS_MOUSE_POS):
                         LEVEL = "EASY"
                         print(LEVEL)
                         LEVEL_BOOL = False
                       
            if event.type == pygame.MOUSEBUTTONDOWN:   
                if LEVEL_HARD.checkForInput(OPTIONS_MOUSE_POS):
                         LEVEL = "HARD"
                         print(LEVEL)
                         LEVEL_BOOL = True
            if event.type == pygame.MOUSEBUTTONDOWN:   
                 if WHITE.checkForInput(OPTIONS_MOUSE_POS):
                          COLOR = 1 
                          Human_turn = True
                          print("play as White")
            if event.type == pygame.MOUSEBUTTONDOWN:   
                 if BLACK.checkForInput(OPTIONS_MOUSE_POS):
                          COLOR = 2
                          Human_turn = False
                          print("play as Black")
                          #set color to black represented by 2
            if event.type == pygame.MOUSEBUTTONDOWN:   
                 if BACK.checkForInput(OPTIONS_MOUSE_POS):
                          main_menu()
                         
                         
                        
        
      
    pygame.display.update()
    clock.tick(60)
    # Quit the game
    pygame.quit()  

def main_menu():
    
    SCREEN.fill(background_color)
# Main game loop
    running = True
    while running:
        pygame.display.update()
        #read mouse position co ordinate
        #all menu buttons rendering
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(120).render("ABALONE", True, Colors.LOGO)
        MENU_RECT = MENU_TEXT.get_rect(center=(620, 120))
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        color = "#D18225"
        board_img =  pygame.image.load("board.png")
    
        board_rect = board_img.get_rect(center=(620,150+MENU_RECT.height//2+60))
        SCREEN.blit(board_img,board_rect)
        PLAY_BUTTON = Button(None, pos=(620, 430), 
                            text_input="PLAY", font=get_font(85), base_color=color, hovering_color="#760101")
        OPTIONS_BUTTON = Button(None, pos=(620, 530), 
                            text_input="SETTINGS", font=get_font(85), base_color=color, hovering_color="#760101")
        QUIT_BUTTON = Button(None, pos=(620, 630), 
                            text_input="EXIT", font=get_font(85), base_color=color, hovering_color="#760101")
        #print(MENU_MOUSE_POS)
        #Button events
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
            
            #event detecton and action
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                     
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                      ok()   
                
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                      options()
                
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                          pygame.quit()
                          sys.exit()
     
    pygame.display.update()
    # Quit the game
    pygame.quit()



main_menu()