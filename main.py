import pygame
from sys import exit

GUI_TEXT_COLOR = 'green'
PAGE_SENSITIVITY = 3
PAGE_FRICTION = 1
MAX_PAGE_SPEED = 20
NOTIFICATION_HIDE_SPEED = 1

class Text:

    def __init__(self, text, size, color, hideSpeed=-1) -> None:
        
        '''
        
        hideSpeed: when it is -1, it wont be hided.

        '''
        
        self.surface = pygame.font.SysFont("comicsansms", size).render(text, False, pygame.color.THECOLORS[color])
        self.rect = self.surface.get_rect()
        self.hideSpeed = hideSpeed
        self.alpha = 255

    def Draw(self, surface):

        if self.hideSpeed != -1 and self.alpha > 0:
            
            self.alpha -= self.hideSpeed
            self.surface.set_alpha(self.alpha)

        surface.blit(self.surface, self.rect)

class Shortcuts:

    def __init__(self, parentRect, *values) -> None:
        
        super().__init__()

        self.surface = pygame.Surface((500, 70 * (len(values) + 1)))
        self.rect = self.surface.get_rect()
        self.rect.center = parentRect.center
        self.alpha = 256

        for i, value in enumerate(values):

            _ = Text(value, 30, 'white')
            _.rect.center = self.rect.width/2, (i+1) * 70
            _.Draw(self.surface)
            
    def Draw(self, surface):
        
        if self.alpha > 0:
                
            self.alpha -= 0.2
            surface.blit(self.surface, self.rect)
            self.surface.set_alpha(self.alpha)

class Application:

    def __init__(self) -> None:
        
        pygame.init()
        pygame.mouse.set_visible(False)

        self.window = pygame.display.set_mode() #flags=pygame.FULLSCREEN
        self.rect = self.window.get_rect()

        self.mode = 1
        self.points = []

        # Drawing Surfaces
        self.drawingSurfaces = [pygame.Surface(self.rect.size)]
        self.drawingSurface = lambda: self.drawingSurfaces[self.drawingIndex]
        self.drawingIndex = 0
        self.drawingSurfaceRect = self.drawingSurface().get_rect()

        # Settings (These can make changeble with GUI in later updates)
        self.color = pygame.color.THECOLORS['yellow']
        self.bgcolor = pygame.color.THECOLORS['black']
        self.penRadius = 2
        self.eraserRadius = 10
        self.lineWidth = 1
        NOTIFICATION_HIDE_SPEED = 1

        # GUI Objects
        self.developerText = Text('Develeoped by Umutcan Ekinci', 14, GUI_TEXT_COLOR)
        self.developerText.rect.center = self.rect.centerx, self.rect.height - self.developerText.rect.height/2 - 5
        self.notificationText = None

        self.shortcuts = Shortcuts(self.rect, 'ESC => Exit', 'CTRL+Z => Undo', 'CTRL+Y => Redo', '1 => Draw with circles', '2 => Draw with lines', '3 => Click draw with lines', '4 => Eraser Mode')

        self.pageSpeed = 0

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

                        self.Undo()
                        self.ShowNotification('Undo')

                elif event.key == pygame.K_y:

                    if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]:

                        self.Redo()
                        self.ShowNotification('Redo')

                elif event.key == pygame.K_1:

                    self.mode = 1
                    self.ShowNotification('Circle Pen Mode')

                elif event.key == pygame.K_2:

                    self.mode = 2
                    self.ShowNotification('Lineer Pen Mode')

                elif event.key == pygame.K_3:

                    self.mode = 3
                    self.ShowNotification('Clickable Lineer Pen Mode')
                    self.notificationText.rect.bottom = self.rect.bottom - 100
                    self.notificationText.rect.centerx = self.rect.centerx

                elif event.key == pygame.K_4:

                    self.mode = 4
                    self.ShowNotification('Eraser Mode')
                    self.notificationText.rect.bottom = self.rect.bottom - 100
                    self.notificationText.rect.centerx = self.rect.centerx

                elif event.key == pygame.K_KP_PLUS:

                    if self.mode == 4:

                        self.eraserRadius += 1    
                        self.ShowNotification('Increase Radius of Eraser')

                    else:
                        
                        self.penRadius += 1
                        self.ShowNotification('Increase Radius of Pen')

                elif event.key == pygame.K_KP_MINUS:

                    if self.mode == 4:
                        if self.eraserRadius > 1:
                            
                            self.eraserRadius -= 1    
                            self.ShowNotification('Decrease Radius of Eraser')

                    else:
                        if self.penRadius > 1:

                            self.penRadius -= 1
                            self.ShowNotification('Decrease Radius of Pen')

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

                # Add page speed for smooth movement
                self.pageSpeed += event.y * PAGE_SENSITIVITY
                
                # Limit Page Speed
                self.pageSpeed = MAX_PAGE_SPEED if (self.pageSpeed > MAX_PAGE_SPEED) else -MAX_PAGE_SPEED if (self.pageSpeed < -MAX_PAGE_SPEED) else self.pageSpeed

    def ShowNotification(self, text):

        self.notificationText = Text(text, 15, 'white', NOTIFICATION_HIDE_SPEED)
        self.notificationText.rect.bottom = self.rect.bottom - 100
        self.notificationText.rect.centerx = self.rect.centerx

    def Undo(self):

        if self.drawingIndex:
                            
            self.drawingIndex -= 1

    def Redo(self):

        if self.drawingIndex + 1 < len(self.drawingSurfaces):
                            
            self.drawingIndex += 1

    def Update(self):

        self.drawingSurfaceRect.y += self.pageSpeed
        
        if self.pageSpeed > PAGE_FRICTION:

            self.pageSpeed -= PAGE_FRICTION

        elif self.pageSpeed < -PAGE_FRICTION:

            self.pageSpeed += PAGE_FRICTION

        else:

            self.pageSpeed = 0

        if self.drawingSurfaceRect.bottom < self.rect.height:

            newSurface = pygame.Surface((self.drawingSurfaceRect.width, self.drawingSurfaceRect.height + self.rect.height))

            for i, surface in enumerate(self.drawingSurfaces):

                _ = newSurface.copy()
                _.blit(surface, (0, 0))
                self.drawingSurfaces[i] = _
                
            self.drawingSurfaceRect.height = newSurface.get_height()

        elif self.drawingSurfaceRect.y > 0:

            newSurface = pygame.Surface((self.drawingSurfaceRect.width, self.drawingSurfaceRect.height + self.rect.height))

            for i, surface in enumerate(self.drawingSurfaces):

                _ = newSurface.copy()
                _.blit(surface, (0, self.rect.height))
                self.drawingSurfaces[i] = _
                
            self.drawingSurfaceRect.height = newSurface.get_height()
            self.drawingSurfaceRect.y -= self.rect.height

    def Draw(self):
        
        # self.DebugLog("Page Speed: " + str(self.pageSpeed) + "  Index: " + str(self.drawingIndex))

        # Draw to drawing surface
        if self.isDrawing:

            if self.mode == 1:

                pygame.draw.circle(self.drawingSurface(), self.color, (self.mousePosition[0], self.mousePosition[1] - self.drawingSurfaceRect.y), self.penRadius)
            
            elif self.mode == 2 or self.mode == 3:
                
                self.points.append((self.mousePosition[0], self.mousePosition[1] - self.drawingSurfaceRect.y))

                if len(self.points) > 1:
                
                    pygame.draw.line(self.drawingSurface(), self.color, self.points[-2], self.points[-1], self.penRadius)
            

            elif self.mode == 4:

                pygame.draw.circle(self.drawingSurface(), self.bgcolor, (self.mousePosition[0], self.mousePosition[1] - self.drawingSurfaceRect.y), self.eraserRadius)            

        elif self.mode == 2:

            self.points.clear()

        # Draw drawing surface
        self.window.blit(self.drawingSurface(), self.drawingSurfaceRect)

        # Draw GUI
        self.developerText.Draw(self.window)
        self.shortcuts.Draw(self.window)

        # Draw cursor
        if self.mode == 4:

            pygame.draw.circle(self.window, self.color, self.mousePosition, self.eraserRadius, 1)

        else:

            pygame.draw.circle(self.window, self.color, self.mousePosition, self.penRadius)

        if self.notificationText:

            self.notificationText.Draw(self.window)

        if hasattr(self, 'log'):

            self.log.Draw(self.window)

    def Exit(self):

        pygame.quit()
        exit()

if __name__ == '__main__':

    Application().Run()