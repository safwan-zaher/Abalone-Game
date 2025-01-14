
def state_value(grid, knocked, turn,AI,ai_moves,hum_moves):

     material_weight = 1.0
     center_weight = 0.2
     mobility_weight = 0.2
   
     if turn <= 10:

       weightgrid =[            [0,0,0,0,0,0],
                               [0,1,1,1,1,1,0],
                              [0,1,2,2,2,2,1,0],
                             [0,1,2,3,3,3,2,1,0],
                            [0,1,2,3,4,4,3,2,1,0],
                           [0,1,2,3,4,5,4,3,2,1,0],
                            [0,1,2,3,4,4,3,2,1,0],
                             [0,1,2,3,3,3,2,1,0],
                              [0,3,2,2,2,2,1,0],
                               [0,3,1,1,1,1,0],
                                [0,0,0,0,0,0]
                                                     ]

     else:

         weightgrid =[      [0,0,0,0,0,0],
                           [0,3,3,3,3,3,0],
                          [0,3,3,3,3,3,3,0],
                         [0,3,3,2,2,2,3,3,0],
                        [0,3,3,2,1,1,2,3,3,0],
                       [0,3,3,2,1,1,1,2,3,3,0],
                        [0,3,3,2,1,1,2,3,3,0],
                         [0,3,3,2,2,2,3,3,0],
                          [0,3,3,3,3,3,3,0],
                           [0,3,3,3,3,3,0],
                            [0,0,0,0,0,0]
                                                 ]

   

    
     knockout_value=0
    
     mobility_value = (ai_moves -  hum_moves) * mobility_weight
     #marble_count
     ai_marble=0
     hum_marble=0
     center_value =0
     for i in range(1,10):
         for j in range(1, len(weightgrid[i]) - 1):
              if grid[i][j] == 2:
                  ai_marble+=1
                  center_value += weightgrid[i][j]
              if grid[i][j] == 1: 
                  hum_marble+=1
     
     material_value = (ai_marble -  hum_marble) * material_weight
     
         
           
    
     if knocked == 1:
        knockout_value=1000
     if knocked==2:
        knockout_value=-1000
         
     state_value = material_value + center_value + mobility_value + knockout_value
     
     return state_value

