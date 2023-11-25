import numpy as np;
import pygame as pg;
from transform import Transform;

class Screen:

    pg.init();

    width = 100;
    height = 100;

    screen_matrix = None;

    window = None;

    def __init__(self, width: int, height: int):
        self.width = width;
        self.height = height;
        self.screen_matrix = np.identity(3);
    
        self.screen_matrix[0] = [self.width/2, 0, self.width/2];
        self.screen_matrix[1] = [0, self.height/2, self.height/2];
        
        self.inverse_screen_matrix = np.linalg.inv(self.screen_matrix);
        

    def ratio(self):
        return self.width / self.height;

    def draw(self, buffer):

        self.window = pg.display.set_mode([self.width, self.height])

        buffer = np.flipud(buffer);
        buffer = np.fliplr(buffer);
        buffer = np.rot90(buffer);
        

        pg.pixelcopy.array_to_surface(self.window, buffer);


    def show(self):

        running = True
        while running:

            # Did the user click the window close button?
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            pg.display.update();

        # Done! Time to quit.
        pg.quit();

    #Converts device coordinates into screen pixel coordinates. 
    def device_to_screen(self, p):
        p = Transform().ensure_numpy_array(p);
        p[2] = 1;
        screen_p = np.dot(self.screen_matrix, p);
        return screen_p;
    
    def screen_to_device(self, p):
        p = Transform().ensure_numpy_array(p);
        device_p = np.dot(self.inverse_screen_matrix, p);
        return device_p;
        
