import argparse
from controller import Controller
import logging
from PyQt5.QtWidgets import QApplication
from gui import Window
from components.board import Board
import generators as gen
from definitions import terrain 

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('--log-level', dest='log_level', default='WARNING', help='log level')

    args, _ = parser.parse_known_args()

    return args

def main(log_level):

    logging.basicConfig(level=log_level)

    play_area = Board(0, 0, 50, 50)
    
    river = gen.generate_river(play_area)
    play_area.add_terrain(river)
    
    cont = Controller(play_area)
    
    
    app = QApplication([])
    window = Window(cont)
    
    app.exec()

if __name__ == '__main__':
    main(**vars(parse_args()))
