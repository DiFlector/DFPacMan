import pygame

pygame.font.init()

class DrawableElement:
    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        pass

    def update(self, x: int, y: int):
        pass

class ImageElement(DrawableElement):
    def __init__(self, img):
        self.img = img

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        screen.blit(self.img, (x, y))
        super().draw_at(screen, screen_width, screen_height, x, y)

    def update(self, x: int, y: int):
        super().update(x, y)


class RepeatingImageElement(ImageElement):
    def __init__(self, img):
        super().__init__(img)

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        for i in range(4):
            for j in range(4):
                super().draw_at(screen, screen_width, screen_height, x + i * self.img.get_width(), y + j * self.img.get_height())

    def update(self, x: int, y: int):
        super().update(x, y)


class AbstractButtonElement(DrawableElement):
    def __init__(self, action, width, height):
        self.action = action
        self.width = width
        self.height = height

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        pass

    def update(self, x, y):
        left, middle, right = pygame.mouse.get_pressed()
        if left:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            if x <= mouse_x <= x + self.width and y <= mouse_y <= y + self.height:
                self.action(x, y, mouse_x, mouse_y)
        super().update(x, y)


class ImageButtonElement(AbstractButtonElement):
    def __init__(self, action, img):
        super(ImageButtonElement, self).__init__(action, img.get_width(), img.get_height())
        self.img = img

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        screen.blit(self.img, (x, y))


class TextElement(DrawableElement):
    def __init__(self, text_getter, size=14, font_name="Comic Sans MS", color=(255, 255, 255)):
        self.text_getter = text_getter
        self.font = pygame.font.SysFont(font_name, size)
        self.color = color

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        text_surface = self.font.render(str(self.text_getter()), True, self.color)
        screen.blit(text_surface, (x, y))

    def update(self, x, y):
        pass


class TextButtonElement(AbstractButtonElement):
    def __init__(self, action, text_element: TextElement, width, height):
        super(TextButtonElement, self).__init__(action, width, height)
        self.text_element = text_element

    def draw_at(self, screen, screen_width, screen_height, x: int, y: int):
        text_width, text_height = self.text_element.font.size(self.text_element.text_getter())
        self.text_element.draw_at(screen, screen_width, screen_height, x + (self.width - text_width) / 2,
                                  y + (self.height - text_height) / 2)
        super().draw_at(screen, screen_width, screen_height, x, y)
