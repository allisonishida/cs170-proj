import os
import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
from student_utils_sp18 import *

"""
======================================================================
  Complete the following function.
======================================================================
"""


def solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_kingdom_names: A list of kingdom names such that node i of the graph corresponds to name index i in the list
        starting_kingdom: The name of the starting kingdom for the walk
        adjacency_matrix: The adjacency matrix from the input file
    Output:
        Return 2 things. The first is a list of kingdoms representing the walk, and the second is the set of kingdoms that are conquered
    """
    leaf_neighbours, to_conquer, to_ignore = leaf_processer(adjacency_matrix)
    
    G = adjacency_matrix_to_graph(adjacency_matrix)
    solution = None
    lowest_cost = float("inf")
    for i in range(0, 100):
        poss_solution = solve_instance(....)
        poss_walk = indices_to_names(poss_solution[0], list_of_kingdom_names)
        cost = cost_of_solution(G, poss_walk, poss_solution[1]) 
        if cost < lowest_cost:
            solution = poss_solution
            lowest_cost = cost
    
    walk = indices_to_names(solution[0])
    conquered_set = solution[1]
    return walk, conquered_set

    raise Exception('"solve" function not defined')
    # return closed_walk, conquered_kingdoms
    
    
"""
======================================================================
  Solve_Instance Functions
======================================================================
"""


def solve_instance(....):
    pass

  
def greedy_step(....):
    pass

def cost(....):
    pass
    
    
"""
======================================================================
  Preprocessing Functions
======================================================================
"""

    
def leaf_processer(adjacency_matrix):
    leaf_neighbours = {}

    for kingdom_index in range(0, len(adjacency_matrix)):
        kingdom = adjacency_matrix[kingdom_index]
        num_nhbrs, nhbrs = neighbours(kingdom, kingdom_index)
        if num_nhbrs == 1:
            nhbr = nhbrs[0]
            nhbr_leaves = None
            if nhbr in leaf_neighbours:
                nhbr_leaves = leaf_neighbours[nhbr]
                nhbr_leaves.append(kingdom_index)
            else:
                nhbr_leaves = [kingdom_index]
            leaf_neighbours[nhbr] = nhbr_leaves

    to_conquer = set()
    to_ignore = set()
    
    for neighbour in leaf_neighbours:
        neighbour_cost = conquer_cost(adjacency_matrix, neighbour)
        leaves_cost = 0
        leaves = leaf_neighbours[neighbour]
        for leaf in leaves:
            leaves_cost += (2 * travel_cost(adjacency_matrix, neighbour, leaf))
            leaves_cost += conquer_cost(adjacency_matrix, leaf)

        if neighbour_cost <= leaves_cost:
            to_conquer.add(neighbour)
            for leaf in leaves:
                to_ignore.add(leaf)

    return list(leaf_neighbours.keys()), to_conquer, to_ignore


def neighbours(am_row, row_index):
    count = 0
    neighbours = []
    for neighbour in range(0, len(am_row)):
        neighbour_dist = am_row[neighbour]
        if neighbour != row_index and neighbour_dist != 'x':
            count += 1
            neighbours.append(neighbour)
    return count, neighbours

def conquer_cost(adjacency_matrix, kingdom_index):
    return adjacency_matrix[kingdom_index][kingdom_index]

def travel_cost(adjacency_matrix, from_kingdom, to_kingdom):
    return adjacency_matrix[from_kingdom][to_kingdom]

  
  
"""
======================================================================
  Helper Functions
======================================================================
"""
 
def indices_to_names(indices, kingdom_names):
    names = []
    for i in indices:
        names.append(kingdom_names[i])
    return names
  
  
  

  
  
"""
======================================================================
   No need to change any code below this line
======================================================================
"""


def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)
    
    input_data = utils.read_file(input_file)
    number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)
    closed_walk, conquered_kingdoms = solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    output_filename = utils.input_to_output(filename)
    output_file = f'{output_directory}/{output_filename}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    utils.write_data_to_file(output_file, closed_walk, ' ')
    utils.write_to_file(output_file, '\n', append=True)
    utils.write_data_to_file(output_file, conquered_kingdoms, ' ', append=True)

def input(input_file):
    input_data = utils.read_file(input_file)
    return data_parser(input_data)



def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
