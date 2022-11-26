# Name: NAME
# Dimensions: 2

import inspect
import math
import random
# --- Set up executable path, do not edit ---
import sys

import numpy as np

this_file_loc = (inspect.stack()[0][1])
main_dir_loc = this_file_loc[:this_file_loc.index('ca_descriptions')]
sys.path.append(main_dir_loc)
sys.path.append(main_dir_loc + 'capyle')
sys.path.append(main_dir_loc + 'capyle/ca')
sys.path.append(main_dir_loc + 'capyle/guicomponents')

# ---

import capyle.utils as utils
from capyle.ca import Grid2D, Neighbourhood, randomise2d

global water_counter
water_counter = 0
# determines how many generations each type of land will burn for 
burn_time_chaparral = 300
burn_time_forest = 370
burn_time_canyon = 80


CHAPARRAL = 2
DENSE_FORREST = 5
LAKE = 3
CANYON = 4
BURNING = 1
BURNT = 0
TOWN = 6

initial_grid=np.ones((100,100),dtype=int)
initial_grid[:,:]=2               # Chapparral
initial_grid[9:34,29:49]= 5       # Dense Forest [y1:y2,x1:x2]
initial_grid[34:39,9:49]= 3       # Lake
initial_grid[39:69,0:49]= 5       # Dense Forest
initial_grid[9:79,59:64]= 4       # Canyon
initial_grid[87:91,37:41]= 6      # Town
initial_grid[0,:]= 0             # Burning  #[y,x]
initial_grid[:,0]= 0             # Burning  #[y,x]
initial_grid[99,:]= 0             # Burning  #[y,x]
initial_grid[:,99]= 0	             # Burning  #[y,x]
#initial_grid[10:25,55:85]= 5       # Dense Forest Extension
#initial_grid[75:87,60:75]= 3       #Lake Extension

start_power_plant=True
start_inciliator=False

#initmat=[[1,98],[98,1],[1,1],[98,98]]
#x=random.randint(0,3)
#r=initmat[x]
if start_power_plant==True:
    initial_grid[1,1]=1
elif start_incillator==True:
    intial_grid[98,1]=1




burn_grid = np.zeros((100, 100))
burn_grid[initial_grid == 2] = burn_time_chaparral
burn_grid[initial_grid == 5] = burn_time_forest
burn_grid[initial_grid == 4] = burn_time_canyon



prob = 0.38


#wind speed
wind_speed = 0.4  #m/s
wind_direction=["NorthWest", "North","NorthEast", "West", "East", "SouthWest", "South", "SouthEast" ] #8 possible wind directions

wind_direction_selected=random.randint(0,7) #program will randomly chosen 1 wind direction out of 8

#slope of terrain
slope_of_dense_forest = math.sin(math.radians(90)) #sin 90 degree

slope_of_chapparell = math.sin(math.radians(180)) #sin 180 degree
slope_of_canyon = math.sin(math.radians(60)) #sin 60 degree

#flammability of terrain
flammability_dense_forest = 7
flammability_chaparell = 4
flammability_canyon = 11

#constant probabilities
constant_prob_dense_forest = 4
constant_prob_chaparell = 3
constant_prob_canyon = 6


#probability formula
probability_burn_chapparell = constant_prob_chaparell*(1 +flammability_chaparell)*wind_speed*slope_of_chapparell
probability_burn_dense_forest = constant_prob_dense_forest*(1 +flammability_dense_forest)*wind_speed*slope_of_dense_forest
probability_burn_canyon = constant_prob_canyon*(1 +flammability_canyon)*wind_speed*slope_of_canyon


   
global prob_grid
prob_grid = np.zeros((100, 100))
for i in range(100):
    for j in range(100):
        if initial_grid[i][j]==2:
             prob_grid[i][j]=probability_burn_chapparell
        elif initial_grid[i][j]==5:
            prob_grid[i][j]=probability_burn_dense_forest
        elif initial_grid[i][j]==4:
            prob_grid[i][j]=probability_burn_canyon
        

	   


def neighbour(pix, neighbourcounts,grid):
    random_numbers = np.random.rand(100, 100)
    if pix == "CHAPARRAL":
        return (((grid == CHAPARRAL)) & (neighbourcounts[BURNING] > 0) & (random_numbers < prob * (0.8 + probability_burn_chapparell)))
    elif pix == "CANYON":
        return (((grid == CANYON)) & (neighbourcounts[BURNING] > 0) & (random_numbers < prob * (0.8 + probability_burn_canyon)))
    else:
        return (((grid == DENSE_FORREST)) & (neighbourcounts[BURNING] > 2) & (random_numbers < prob * (0.8 + probability_burn_dense_forest)))


def transition_function(grid, neighbourstates, neighbourcounts, burn_grid):

    NW, N, NE, W, E, SW, S, SE = neighbourstates

    burning_cells = (grid == BURNING)
    burn_grid[burning_cells] -= 1

    burnt = burning_cells & (burn_grid == 0)

    neighbours1 =  neighbour("CHAPARRAL", neighbourcounts,grid)
    neighbours2 = neighbour("CANYON", neighbourcounts,grid)
    neighbours3 = neighbour("DENSE_FORREST", neighbourcounts,grid)

    grid[neighbours1] = BURNING
    grid[neighbours2] = BURNING
    grid[neighbours3] = BURNING

        
    
    grid[burnt] = BURNT
    return grid


def setup(args):
    config_path = args[0]
    config = utils.load(config_path)
    # ---THE CA MUST BE RELOADED IN THE GUI IF ANY OF THE BELOW ARE CHANGED---
    config.title = "Conway's game of life"
    config.dimensions = 2
    config.states = (0,         # Burnt
                       1,         # Burning
                     2,         # Chapparral
                     3,         # Lake
                     4,         # Canyon 
                     5,         # Dense Forest
                     6,         # Town
                     )
    # ------------------------------------------------------------------------

    # ---- Override the defaults below (these may be changed at anytime) ----

    config.state_colors = [
                        (0,0,0),		       # Burnt
                        (1,0,0),               # Burning
                        (0.6, 0.6, 0),         # Chapparral
                        (0.1, 0.7, 1),         # Lake
                        (1, 1, 0),             # Canyon
                        (0.2, 0.3, 0),         # Dense Forest
                        (0,0,0)                # Town
                            ]

    config.num_generations = 1000
    config.grid_dims = (100,100)
    config.set_initial_grid(initial_grid)

    # ----------------------------------------------------------------------

    if len(args) == 2:
        config.save()
        sys.exit()

    return config


# def slope_probability_func(self):
#     slope_probability = np.exp(self.aConstant*self.theta)
#     theta1 = np.arctan(elevation1, ele)

#     return slope_probability


def main():
    """ Main function that sets up, runs and saves CA"""
    # Get the config object from set up
    config = setup(sys.argv[1:])

    # Create grid object
    grid = Grid2D(config, (transition_function, burn_grid))

    # Run the CA, save grid state every generation to timeline
    timeline = grid.run()

    # save updated config to file
    config.save()
    # save timeline to file
    utils.save(timeline, config.timeline_path)



if __name__ == "__main__":
    main()
