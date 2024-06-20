import config

import logging

logger = logging.getLogger(__name__)
class Node:

    def __init__(self, x, y, parent=None):

        self._x = x
        self._y = y
        self._parent = parent
        self._g_score = None
        self._h_score = None

    def __repr__(self):
        return '(%s, %s)' %(self._x, self._y)



    def set_parent(self, parent):
       self._parent = parent

    def get_parent(self):
        return self._parent

    def get_coordinates(self):
        return self._x, self._y

    def set_g_score(self, score):
        self._g_score = score

    def set_h_score(self, score):
        self._h_score = score

    def get_score(self):
        if self._g_score is None or self._h_score is None:
            raise AttributeError('Both G score and H score mustbe set')
        return self._g_score + self._h_score

class PathFinder:

    def __init__(self, board):
        self._board = board

    def find_path(self, travel_efficiencies, start, need):


        # FIXME should check both sites and terrain
        terrain_type = config.TERRAIN_PROVIDES.get(need)
        if terrain_type is None:
            logger.error('Cannot determine source for need %s', need)
            raise RuntimeError 

        destintations = self._board.get_terrain_shape(terrain_type)
        logger.debug('Find path from %s to %s', start, destintations)

        open_nodes = []
        closed_nodes = []
    
        start_node = Node(start[0], start[1])
    
        open_nodes.append(start_node)
    
        n_iter = 0
        while n_iter < 100:
            n_iter += 1
    
            this_node = open_nodes[0]
    
            for tr in config.BOARD_TRANSLATIONS:
                check_node = Node(start[0]+tr[0], start[1]+tr[1], this_node)
    
                if check_node in closed_nodes:
                    continue

                logger.debug('Check node %s', check_node)
    
                # check with the board if this node is valid
                if self._board.is_valid(this_node.get_coordinates()):
                    # check if this node is on the open list and if so do something
                    # get the movement cost for this node
                    g_score = ()
    
                # calculate the heuristic
                h_score = manhattan_distance_score(check_node.get_coordinates(), end)
    
                check_node.set_g_score(g_score)
                check_node.set_h_score(h_score)
    
                open_nodes.append(check_node)
    
            open_nodes.remove(this_node)
            closed_nodes.append(this_node)
    
            open_nodes.sort()
