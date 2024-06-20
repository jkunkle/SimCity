import math
from PyQt5.QtWidgets import QMainWindow, QFrame, QApplication, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QDockWidget
from PyQt5.QtCore import pyqtSignal, QObject, QThread, Qt, QBasicTimer
from PyQt5.QtGui import QPainter, QColor
#from PyQt5.QtGui import QFrame
from states import GuiState
from connection import Road
from gui_config import GuiColors
from definitions import zone_types, connection_types, terrain

class Window(QMainWindow):
    def __init__(self, controller):
        super(Window, self).__init__()

        self._controller = controller

        #self._controller.set_time_callback(self.update_time)
        # creating a board object
        self._gui_board = GUIBoard(self, controller.board)
        self.timer = QBasicTimer()
        self.timer.start(100, self)
        # creating a status bar to show result
        self.statusbar = self.statusBar()
        self.action_menu = QDockWidget('action menu', self)
        self.action_widget = QWidget(self)
        self.action_layout = QVBoxLayout()
        #self.action_menu = QDockWidget('test', self, Qt.LeftDockWidgetArea)
        self.button_road = QPushButton('Dirt Road', self)
        self.button_road.clicked.connect(self.clicked_dirt_road)
        self.button_farm = QPushButton('Farm', self)
        self.button_farm.clicked.connect(self.clicked_farm)

        self.action_layout.addWidget(self.button_road)
        self.action_layout.addWidget(self.button_farm)

        self.action_widget.setLayout(self.action_layout)

        self.action_menu.setWidget(self.action_widget)
        #self.action_menu.setWidget(self.button_road)
        #self.action_menu.setWidget(self.button_farm)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.action_menu)

        self._state = GuiState.neutral
        
        # adding border to the status bar
        self.statusbar.setStyleSheet('border: 2px solid black')
        
        # calling showMessage method when signal received by board
        self._gui_board._clicked_signal[int, int].connect(self.board_clicked)
        self._gui_board._terminate_signal[int].connect(self.reset_state)
        
        # adding board as a central widget
        self.setCentralWidget(self._gui_board)
        
        # setting title to the window
        self.setWindowTitle('')
        
        # setting geometry to the window
        self.setGeometry(100, 100, 600, 400)
        
        #self.countBtn = QPushButton("Click me!", self)
        #self.countBtn.clicked.connect(self.start_worker)
        #
        #self.centralWidget = QWidget()
        #self.setCentralWidget(self.centralWidget)
        #layout = QVBoxLayout()
        #layout.addWidget(self.countBtn)

        #self.centralWidget.setLayout(layout)
        # showing the main window
        self.show()
        self.statusbar.showMessage('test')

    def get_controller(self):
        return self._controller

    def clicked_dirt_road(self):
        self._state = GuiState.build_dirt_road
    def clicked_farm(self):
        self._state = GuiState.build_farm

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():

            self._controller.run_step()

            self.update_time(self._controller.get_time())
            #self._gui_board.update()
    def reset_state(self, stat=True):
        self._state = GuiState.neutral

    def board_clicked(self, x, y):

        if self._state == GuiState.build_dirt_road:
            self._controller.board.add_path(Road([(x, y)], connection_types.dirt_road))
        if self._state == GuiState.build_farm:
            self._controller.board.add_zone((x, y), zone_types.farm)

        self._gui_board.update()


    def update_time(self, time):
        self.statusbar.showMessage(str(time))

class GUIBoard(QFrame):

    _clicked_signal = pyqtSignal(int, int)
    _terminate_signal = pyqtSignal(int)
    # constructor
    def __init__(self, parent, board):
        super(GUIBoard, self).__init__(parent)

        # setting focus
        self.setFocusPolicy(Qt.StrongFocus)
        self._color = QColor('green')
        self._board = board
        self._controller = parent.get_controller()
        # creating painter object

    # square width method
    def square_width(self):
        return self.contentsRect().width() / self._board.x_span

    # square height
    def square_height(self):
        return self.contentsRect().height() / self._board.y_span

    def get_square_id(self, x, y):

        square_x = math.floor(x*self._board.x_span/self.contentsRect().width())

        square_y = math.floor(y*self._board.y_span/self.contentsRect().height())

        return square_x, square_y

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:

            x, y = self.get_square_id(event.x(), event.y())

            self._clicked_signal.emit(x, y)
        if event.button() == Qt.RightButton:
            self._terminate_signal.emit(True)

    # start method
    #def start(self):
    #    # msg for status bar
    #    # score = current len - 2
    #    self.msg2statusbar.emit(str(len(self.snake) - 2))

    #    # starting timer
    #    self.timer.start(GUIBoard.SPEED, self)

    # paint event
    def paintEvent(self, event):
        painter = QPainter(self)

        # getting rectangle
        #rect = self.contentsRect()

        #self.fill_square(painter, 0, 0, 'green')
        # board top
        self.fill_board(painter, GuiColors.empty)
        #for x in range(self._shape.get_xmin(), self._shape.get_xmax()):
        #    for y in range(self._shape.get_ymin(), self._shape.get_ymax()):
        #        self.fill_square(painter, x, y, GuiColors.empty)

        for ter in self._controller.board.terrain:
            if ter.type == terrain.water:
                for x, y in ter.iter_points():
                    self.fill_square(painter, x, y, GuiColors.water)

        for path in self._controller.board.paths:
            if path.get_type() == connection_types.dirt_road:
                for x, y in path.iter_points():
                    self.fill_square(painter, x, y, GuiColors.dirt_road)

        for zone in self._controller.board.get_zones():
            for x, y in zone.iter_points():
                self.fill_square(painter, x, y, GuiColors.farm)

            for site in zone.sites:
                for x, y in site.iter_points():
                    self.fill_small_square(painter, x, y, 'black')


    def fill_small_square(self, painter, sq_x, sq_y, color):

        x_min, y_min, x_size, y_size = self._get_small_square_dimensions(sq_x, sq_y)

        painter.fillRect(x_min, y_min, x_size, y_size, QColor(color))

    # drawing square
    def fill_square(self, painter, sq_x, sq_y, color):

        x_min, y_min, x_size, y_size = self._get_square_dimensions(sq_x, sq_y)

        # painting rectangle
        painter.fillRect(x_min, y_min, x_size, y_size, QColor(color))

    def fill_board(self, painter, color):
        painter.fillRect(0, 0, self.contentsRect().width()+1,self.contentsRect().height()+1, QColor(color))


    def _get_small_square_dimensions(self, x, y):

        x_min, y_min, x_size, y_size = self._get_square_dimensions(x, y)

        x_min_sm = x_min + x_size/4
        y_min_sm = y_min + y_size/4
        x_size_sm = x_size/2
        y_size_sm = y_size/2

        return x_min_sm, y_min_sm, x_size_sm, y_size_sm

    def _get_square_dimensions(self, x, y):
        rect = self.contentsRect()
        x_min = int(rect.left()+ x*self.square_width())
        y_min = int(rect.top() + y*self.square_height())

        x_size = self.square_width()+1
        y_size = self.square_height()+1

        return x_min, y_min, x_size, y_size

