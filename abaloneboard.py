import pygame
import math
import Colors
import copy
from Values import state_value
from Node import Node


class Board:

    def __init__(self, center, len, screen, dims):
        self.center = center
        self.len = int(len)
        self.screen = screen
        self.ball_r = int(dims[0])
    
        self.field_r = self.ball_r - 6

        self.gap = int(dims[1])
        
        self.allowedMoves = [[0,1],[0,1,1],[0,1,1,1],[0,1,1,2],[0,1,1,1,2],[0,1,1,1,2,2],[0,2],[0,2,2],[0,2,2,2],[0,2,2,2,1],[0,2,2,2,1,1],[0,2,2,1]]
        
        self.allowedKnocks = [[0,1,1,2],[0,1,1,1,2],[0,1,1,1,2,2],[0,2,2,1],[0,2,2,2,1],[0,2,2,2,1,1]]
        
        self.deleted = 0
        self.scoreHum = 0
        self.scoreAI = 0
        self.turn_counter = 0
        #h = sin60*len
        
        self.vertices = [(self.center[0] - self.len/2, self.center[1] - self.len*math.sqrt(3)/2), # draw the boundaries
                        (self.center[0] + self.len/2, self.center[1] - self.len*math.sqrt(3)/2),
                        (self.center[0] + self.len, self.center[1]),
                       (self.center[0] + self.len/2, self.center[1] + self.len*math.sqrt(3)/2),
                      (self.center[0] - self.len/2, self.center[1] + self.len*math.sqrt(3)/2),
                     (self.center[0] - self.len, self.center[1])]

                 

        self.boardState = [[9,9,9,9,9,9], #to examine the state of the game
                          [9,2,2,2,2,2,9],
                         [9,2,2,2,2,2,2,9],
                        [9,0,0,2,2,2,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                      [9,0,0,0,0,0,0,0,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                        [9,0,0,1,1,1,0,0,9],
                         [9,1,1,1,1,1,1,9],
                          [9,1,1,1,1,1,9],
                           [9,9,9,9,9,9]]

        self.resultState = [[9,9,9,9,9,9],
                          [9,2,2,2,2,2,9],
                         [9,2,2,2,2,2,2,9],
                        [9,0,0,2,2,2,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                      [9,0,0,0,0,0,0,0,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                        [9,0,0,1,1,1,0,0,9],
                         [9,1,1,1,1,1,1,9],
                          [9,1,1,1,1,1,9],
                           [9,9,9,9,9,9]]

        self.grid =     [[2,2,2,2,2],   # denotes the inner board grid
                        [2,2,2,2,2,2],
                       [0,0,2,2,2,0,0],
                      [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                       [0,0,1,1,1,0,0],
                        [1,1,1,1,1,1],
                         [1,1,1,1,1]]

        self.coords =   [[2,2,2,2,2],  # to store the valid co ordinates of the ball
                        [2,2,2,2,2,2],
                       [0,0,2,2,2,0,0],
                      [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                       [0,0,1,1,1,0,0],
                        [1,1,1,1,1,1],
                         [1,1,1,1,1]]

    def initCoords(self):
        for i in range(9):
            if i == 0:
                curCoord = (int(self.center[0] - int(4*self.ball_r + 2*self.gap)), int(self.center[1] - 8*self.ball_r))
            if i < 5 and i != 0:
                curCoord = (curCoord[0] - int(self.ball_r + self.gap/2), curCoord[1] + 2*self.ball_r)
            if i >= 5:
                curCoord = (curCoord[0] + int(self.ball_r + self.gap/2), curCoord[1] + 2*self.ball_r)
            for j in range(len(self.coords[i])):
                self.coords[i][j] = int(curCoord[0] + (j)*(2*self.ball_r + self.gap)),int(curCoord[1])
            #print(self.coords)    

    def initialize(self):
        self.initCoords()

    def draw(self, current_ball, color_1, color_2):
        pygame.draw.polygon(self.screen, Colors.BROWN, self.vertices) # drew the background
        
        for i in range(9): # draw the balls
            for j in range(len(self.grid[i])):
                
                if self.boardState[i + 1][j + 1] == 0: # to draw the blank space
                    self.grid[i][j] = pygame.draw.circle(self.screen, Colors.LIGHTBROWN, self.coords[i][j], self.field_r)
                if self.boardState[i + 1][j + 1] == 1: # to draw balls for human side
                    self.grid[i][j] = pygame.draw.circle(self.screen, color_2, self.coords[i][j], self.ball_r)
                if self.boardState[i + 1][j + 1] == 2:  # to draw balls for AI
                    self.grid[i][j] = pygame.draw.circle(self.screen, color_1, self.coords[i][j], self.ball_r)
        for i in range(self.scoreHum):
            #  pygame.draw.circle(self.screen, color_2, (270 + i*(2*self.ball_r + self.gap), 120), self.ball_r)
             pygame.draw.circle(self.screen, color_2, (52 + i*(self.ball_r + 4*self.gap), 220), self.ball_r)


        for i in range(self.scoreAI): # draw when a point is hit
            # print("CHECK")
            pygame.draw.circle(self.screen, color_1, (1000 + i*(self.ball_r + 4*self.gap), 220), self.ball_r)

        if current_ball != 0:
            pygame.draw.circle(self.screen, Colors.GREEN, self.coords[current_ball[0]][current_ball[1]], self.ball_r)
        
        
        #print(self.grid[0][0])
    
    def check_move(self,coords1 , coords2):
        
        origx = coords1[1]+1
        origy = coords1[0]+1
        #origx,origy is the current selected ball position in the boardstate
        x1 = coords1[1] + 1
        y1 = coords1[0] + 1
        x2 = coords2[1] + 1
        y2 = coords2[0] + 1
        
        dir=[0,0] #default direction 0,0
        
        resultState = copy.deepcopy(self.boardState) #copying boardstate into resultstate 
        
        player = resultState[y1][x1]#direction define
        
        #(x1,y1)->(x1+1,y1) direction in right x-axis (represented by +1)
        if x1 < x2 : dir[1] = 1 #dir[1] x axis ( column) 
        #(x1,y1)->(x1-1,y1) direction in left  x-axis(represented by -1)
        if x1 > x2: dir[1] = -1
        if y1 > y2: dir[0] = -1  # direction in up  y-axis(represented by -1)
        if y1 < y2: dir[0]=1 # direction in up  y-axis(represented by 1)
        
        if abs(y2 - y1) > 1 or abs(x2 - x1) > 1: return [False] #cant movemore than one step

        moveseq = []
        coordlist = []
        deleted = 0
        moveseq.append(0)
        coordlist.append([origy, origx]) #current selected ball position
        moveseq.append(resultState[y1][x1]) # movelist contain the series of balls to move
                                             # 0112
        coordlist.append([y2, x2]) #append next ball position   

        while True:
             
                if resultState[y2][x2] == 0: #if the selected mouse position is empty ,that is no other ball is there
                     for i in self.allowedMoves:
                         if moveseq == i:
                                #  print("i " , i)
                                #  print("seq",moveseq)
                                 for j in range(len(moveseq)):
                                     resultState[coordlist[j][0]][coordlist[j][1]] = moveseq[j]
                                
                                 #print (resultState)
                                 return [True, resultState, [moveseq, coordlist, deleted]]  
                     return [False]   
                                   
               
                
                if resultState[y2][x2] == 9: #if boundary then check if it is allowed to knock out the corner ball
                   for i in self.allowedKnocks:
                     if moveseq == i: 
                         deleted = moveseq.pop()
                         coordlist.pop()
                         for j in range(len(moveseq)):
                            resultState[coordlist[j][0]][coordlist[j][1]] = moveseq[j]
                            
                         return [True, resultState, [moveseq, coordlist, deleted]]
                   return [False]
               
                
                else:
                    
                    moveseq.append(resultState[y2][x2])
                    #print(moveseq)
                
                    if x1 > x2: dir[1] = -1
                    if x1 < x2: dir[1] = 1
                    if y1 == y2: dir[0] = 0
                    if y1 > y2: dir[0] = -1
                    if y1 < y2: dir[0] = 1

                    x1 = x2
                    y1 = y2

                # y <= 5

                    if y1 < 5 and dir[0] == -1 and dir[1] == -1:
                        x2 = x1 - 1
                    elif y1 < 5 and dir[0] == -1 and dir[1] == 1:
                        x2 = x1
                    elif y1 < 5 and dir[0] == 1 and dir[1] == 1:
                        x2 = x1 + 1
                    elif y1 < 5 and dir[0] == 1 and dir[1] == -1:
                        x2 = x1
               

                # y > 5

              
                    elif y1 > 5 and dir[0] == -1 and dir[1] == -1:
                          x2 = x1
                    elif y1 > 5 and dir[0] == -1 and dir[1] == 1:
                          x2 = x1 + 1
                    elif y1 > 5 and dir[0] == 1 and dir[1] == 1:
                          x2 = x1
                    elif y1 > 5 and dir[0] == 1 and dir[1] == -1:
                          x2 = x1 - 1


                # y == 5

                    elif y1 == 5 and ((dir[0] == -1 and dir[1] == 1) or (dir[0] == 1 and dir[1] == 1)):
                        x2 = x1
                    elif y1 == 5 and ((dir[0] == -1 and dir[1] == -1) or (dir[0] == 1 and dir[1] == -1)):
                         x2 = x1 - 1
                    elif y1 == 5 and dir[0] == 1 and dir[1] == 0: #ok
                        x2 = x1 - 1
                    elif y1 == 5 and dir[0] == -1 and dir[1] == 0: #ok
                        x2 = x1 - 1
                    else:
                        x2 = x1 + dir[1] 

                    y2 = y1 + dir[0]
                
                          
                            

                     
                    coordlist.append([y2, x2])
                    #print([x1,y1],[x2,y2])
                        
                            
        
        
    def make_move(self, result):
        moveseq = result[0]
        coordlist =result[1]
        deleted = result[2]
        self.deleted = deleted
        if deleted == 1:
            self.scoreAI += 1
        elif deleted == 2:
            self.scoreHum += 1
        for i in range(len(moveseq)):
            self.boardState[coordlist[i][0]][coordlist[i][1]] = moveseq[i] 
            
    def generate_moves(self, grid, player):

        all = [[1,0],[0,-1],[0,1],[-1,0]] # directions common in all case
        y_less_5 = [[1,1],[-1,-1]] + all  #when y<5 2 case / up[1,1] and 
        y_grt_5 = [[-1,1],[1,-1]] + all
        y_eql_5 = [[1,-1],[-1,-1]] + all
        legal_moves = []
        result = []

        for i in range(1,10):
            for j in range(1, len(grid[i]) - 1):
                if grid[i][j] == player:
                    #print("for grid", i,j)
                    if i > 5:
                        for k in y_grt_5:
                            #print("for ",k)
                            dx = k[1]
                            dy = k[0]
                            if grid[i + dy][j + dx] != 9:
                                #print("checking1" , i+dy , j+dx)
                                result = self.check_move([i - 1,j- 1],[i + dy- 1, j + dx- 1])
                                #print("checking2",i-1 , j-1)
                               
                                #print("checking3",i + dy- 1, j + dx- 1)
                                if result[0]:
                                    #print("legal" ,result[0],result[1])
                                    
                                    legal_moves.append([result[1],result[2]])
                                    
                                   
                            #print("legal",legal_moves)
                    

                    elif i < 5:
                        for k in y_less_5:
                            dx = k[1]
                            dy = k[0]
                            if grid[i + dy][j + dx] != 9:
                                result = self.check_move([i - 1,j- 1],[i + dy- 1, j + dx- 1])
                                if result[0]:
                                    legal_moves.append([result[1],result[2]])

                    else:
                        for k in y_eql_5:
                            dx = k[1]
                            dy = k[0]
                            if grid[i + dy][j + dx] != 9:
                                result = self.check_move([i - 1,j- 1],[i + dy- 1, j + dx- 1])
                                if result[0]:
                                    legal_moves.append([result[1],result[2]])
        # print("LEGAL MOVES : ", legal_moves)
        return legal_moves
    
    
    def minimax(self, depth, starting_node, isMaximizingPlayer, alpha, beta):

        #  new_move = board.minimax(3, root, False, float('-inf'),float('inf')).move

        if depth == 0:
            return starting_node
        else:
            if isMaximizingPlayer:
                #

                # class Node:
                #     def __init__(self, grid, move, value, children):
                #         self.grid = grid
                #         self.move = move
                #         self.value = value
                #         self.children = children

                bestNode = Node([],[],float('-inf'),[])
                legal_moves = self.generate_moves(starting_node.nodestate, 2) #check all legal moves 

                for move in legal_moves:
                    #move[0] -> the boardstate after playing the move
                    #move[1]-> moveseq ,coordlist,deleted
                    #ai_moves=len(self.generate_moves(move[0], 2))
                    #hum_moves=len(self.generate_moves(move[0], 1))
                    newNode = Node(move[0], move[1], state_value(move[0], move[1][2], self.turn_counter,isMaximizingPlayer,ai_moves=0,hum_moves=0), [])
                    starting_node.children.append(newNode)
                for node in starting_node.children:
                    nextNode = self.minimax(depth - 1, node, False, alpha, beta)
                    if nextNode.value > bestNode.value:
                        bestNode = nextNode
                    alpha = max(alpha, bestNode.value)
                    if beta <= alpha:
                        break
                return bestNode
            else:
                bestNode = Node([],[],float('inf'),[])
                legal_moves = self.generate_moves(starting_node.nodestate, 1)

                for move in legal_moves:
                    #ai_moves=len(self.generate_moves(move[0], 2))
                    #hum_moves=len(self.generate_moves(move[0], 1))
                    newNode = Node(move[0], move[1], state_value(move[0], move[1][2], self.turn_counter,isMaximizingPlayer,ai_moves=0,hum_moves=0), [])
                    starting_node.children.append(newNode)
                for node in starting_node.children:
                    nextNode = self.minimax(depth - 1, node, True, alpha, beta)
                    if nextNode.value < bestNode.value:
                        bestNode = nextNode
                    beta = min(beta, bestNode.value)
                    if beta <= alpha:
                        break
                return bestNode
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
