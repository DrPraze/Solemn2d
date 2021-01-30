import pygame
from time import sleep
try:
    import Image
except ImportError:
    from PIL import Image
from PIL import ImageTk
from tkinter.messagebox import showerror

class anime:
    pygame.init()

    def animate(images, fps):
        try:
            def get_pic_size(filename):
                image = Image.open(filename)
                width, height = image.size
                return width, height

            imagelist = [i for i in images]
            try:
                size = get_pic_size(imagelist[1])
            except IndexError:
                showerror('An Error Occured', 'there are no frames to animate')
            # print(size)
            screen = pygame.display.set_mode((size))
            logo = pygame.image.load('imgs\\skeleton.jpg')
            pygame.display.set_icon(logo)
            pygame.display.set_caption("Project Preview - Skeleton 2D")
            imagelist = []
            for i in images:
                imagelist.append(i)
            for i in imagelist:
                img = pygame.image.load(i)
                screen.blit(img, [0, 0])
                sleep(fps)
                pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        #Skeleton()
                    pygame.display.update()
        except pygame.error:
            pass

        """
        def Test(self):
            #====================TESTS===========================
            images = [i for i in glob("*.jpg")]
            for i in images:
                self.animate(images, fps =1)
            #==================END OF REGION===============
        """
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()
            pygame.display.flip()
