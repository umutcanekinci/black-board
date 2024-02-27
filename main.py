import pygame
from sys import exit

GUI_TEXT_COLOR = 'green'
MOUSE_WHEEL_SENSITIVITY = 10

class Text:

    def __init__(self, text, size, color) -> None:
        
        self.surface = pygame.font.SysFont("comicsansms", size).render(text, False, pygame.color.THECOLORS[color])
        self.rect = self.surface.get_rect()

    def Draw(self, surface):

        surface.blit(self.surface, self.rect)

class Application:

    def __init__(self) -> None:
        
        pygame.init()
        pygame.mouse.set_visible(False)

        self.window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.rect = self.window.get_rect()

        # Drawing Surfaces
        self.drawingSurfaces = [pygame.Surface(self.rect.size)]
        self.drawingSurface = lambda: self.drawingSurfaces[self.drawingIndex]
        self.drawingIndex = 0
        self.drawingSurfaceRect = self.drawingSurface().get_rect()

        # Writing color
        self.color = pygame.color.THECOLORS['yellow']

        # GUI Objects
        self.developerText = Text('Develeoped by Umutcan Ekinci', 14, GUI_TEXT_COLOR)
        self.developerText.rect.center = self.rect.centerx, self.rect.height - self.developerText.rect.height/2 - 5
    
        self.tutorialText = Text('ESC => Exit\nCTRL+Z => Undo', 14, GUI_TEXT_COLOR)

    def DebugLog(self, text):

        self.log = Text(str(text), 15, 'white')

    def Run(self):

        self.isRunning = True
        self.isDrawing = False

        while self.isRunning:

            self.HandleEvents()
            self.Update()
            self.Draw()
            pygame.display.update()

    def HandleEvents(self):

        for event in pygame.event.get():

            # Get mouse position
            self.mousePosition = pygame.mouse.get_pos()
            self.keys = pygame.key.get_pressed()

            if event.type == pygame.QUIT:

                self.Exit()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    
                    self.Exit()

                elif event.key == pygame.K_z:
                    
                    if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]:

                        if self.drawingIndex:
                            
                            self.drawingIndex -= 1

            elif event.type == pygame.MOUSEBUTTONDOWN:
                
                #1 - left click
                #2 - middle click
                #3 - right click
                #4 - scroll up
                #5 - scroll down

                if event.button == 1:

                    self.drawingSurfaces = self.drawingSurfaces[:self.drawingIndex+1]
                    self.drawingSurfaces.append(self.drawingSurface().copy())
                    self.drawingIndex += 1
                    self.isDrawing = True

            elif event.type == pygame.MOUSEBUTTONUP:

                #1 - left click
                #2 - middle click
                #3 - right click
                #4 - scroll up
                #5 - scroll down

                if event.button == 1:

                    self.isDrawing = False

            elif event.type == pygame.MOUSEWHEEL:

                self.drawingSurfaceRect.y += event.y * MOUSE_WHEEL_SENSITIVITY
                
                if self.drawingSurfaceRect.bottom < self.rect.height:

                    newSurface = pygame.Surface((self.drawingSurfaceRect.width, self.drawingSurfaceRect.height + self.rect.height))
                    newSurface.fill(pygame.color.THECOLORS['brown'])
                    newSurface.blit(self.drawingSurface(), (0, 0))
                    self.drawingSurfaces[self.drawingIndex] = newSurface
                    
                    self.drawingSurfaceRect.height = newSurface.get_height()

                elif self.drawingSurfaceRect.y > 0:

                    newSurface = pygame.Surface((self.drawingSurfaceRect.width, self.drawingSurfaceRect.height + self.rect.height))
                    newSurface.fill(pygame.color.THECOLORS['red'])
                    newSurface.blit(self.drawingSurface(), (0, self.rect.height))
                    self.drawingSurfaces[self.drawingIndex] = newSurface
                    
                    self.drawingSurfaceRect = newSurface.get_rect()
                    self.drawingSurfaceRect.y = -self.rect.height

    def Update(self):

        pass
        
    def Draw(self):
        
        self.DebugLog(self.drawingIndex)

        # Draw to drawing surface
        if self.isDrawing:

            pygame.draw.circle(self.drawingSurface(), self.color, (self.mousePosition[0], self.mousePosition[1] - self.drawingSurfaceRect.y), 2)

        # Draw drawing surface
        self.window.blit(self.drawingSurface(), self.drawingSurfaceRect)

        self.developerText.Draw(self.window)

        # Draw cursor
        pygame.draw.circle(self.window, self.color, self.mousePosition, 4)

        if hasattr(self, 'log'):

            self.log.Draw(self.window)

    def Exit(self):

        pygame.quit()
        exit()

if __name__ == '__main__':

    Application().Run()