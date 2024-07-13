from config import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf= pygame.Surface((tamanho_bloco, tamanho_bloco)), groups=None):
        super().__init__(groups)

        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.old_rect = self.rect.copy()


class Plataforma_Movel(Sprite):
    def __init__(self, groups, pos_inicial, pos_final, direcao_movi, Vel):
        surf = pygame.Surface((30, 10))

        super().__init__(pos_inicial, surf, groups)

        self.rect.center = pos_inicial
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.Vel = Vel

        #maneira de diferenciar os sprites entre si
        self.moving = True
        self.direcao = vector(1, 0) if direcao_movi == "x" else vector(0, 1)
        self.direcao_movi = direcao_movi

    def check_borda(self):

        #indo para a direita/horizontal
        if self.direcao_movi == "x":
            if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                self.direcao.x = -1
                self.rect.right = self.pos_final[0]
            if self.rect.right <= self.pos_inicial[0] and self.direcao.x == -1:
                self.direcao.x = 1
                self.rect.right = self.pos_inicial[0]
                #vertical
        if self.direcao_movi == "y":
            if self.rect.top >= self.pos_final[1] and self.direcao.y == 1:
                self.direcao.y = -1
                self.rect.top = self.pos_final[1]
            if self.rect.top <= self.pos_inicial[1] and self.direcao.y == -1:
                self.direcao.y = 1
                self.rect.top = self.pos_inicial[1]

    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.image.fill("white")
        self.rect.topleft += self.direcao * self.Vel * dt
        self.check_borda()


class DanoReset(Sprite):
    def __init__(self, groups, pos_inicial, pos_final, direcao_movi, Vel, image):
        self.image = image
        super().__init__(pos_inicial, image, groups)

        self.rect.center = pos_inicial
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.Vel = Vel

        #maneira de diferenciar os sprites entre si
       # self.move = True
        self.direcao = vector(1, 0) if direcao_movi == "x" else vector(0, 1)
        self.direcao_movi = direcao_movi

    def check_borda(self):

        #indo para a direita/horizontal
        if self.direcao_movi == "x":
            if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                self.rect.right = self.pos_inicial[0]

            if self.rect.right <= self.pos_final[0] and self.direcao.x == -1:
                self.rect.right = self.pos_inicial[0]
                #vertical
        if self.direcao_movi == "y":
            if self.rect.top >= self.pos_final[1] and self.direcao.y == 1:

                self.rect.top = self.pos_inicial[1]
            if self.rect.top <= self.pos_inicial[1] and self.direcao.y == -1:
                self.rect.top = self.pos_inicial[1]

    def update(self, dt):
        self.old_rect = self.rect.copy()

        self.rect.topleft += self.direcao * self.Vel * dt
        self.check_borda()

class ObjParado(Sprite):
    def __init__(self, pos, groups,image):
        self.image = image
        super().__init__(pos, image, groups)


class DanoContinuo(Sprite):
    def __init__(self, groups, pos_inicial, pos_final, direcao_movi, Vel, image):
        self.image = image
        super().__init__(pos_inicial, image, groups)

        self.rect.center = pos_inicial
        self.pos_inicial = pos_inicial
        self.pos_final = pos_final
        self.Vel = Vel

        #maneira de diferenciar os sprites entre si
       # self.move = True
        self.direcao = vector(1, 0) if direcao_movi == "x" else vector(0, 1)
        self.direcao_movi = direcao_movi

    def check_borda(self):

        #indo para a direita/horizontal
        if self.direcao_movi == "x":
            if self.rect.right >= self.pos_final[0] and self.direcao.x == 1:
                self.direcao.x = -1
                self.rect.right = self.pos_final[0]
                pygame.transform.flip(self.image, True, False)
            if self.rect.right <= self.pos_inicial[0] and self.direcao.x == -1:
                self.direcao.x = 1
                self.rect.right = self.pos_inicial[0]
                pygame.transform.flip(self.image, True, False)
                # vertical
        if self.direcao_movi == "y":
            if self.rect.top >= self.pos_final[1] and self.direcao.y == 1:
                self.direcao.y = -1
                self.rect.top = self.pos_final[1]
                pygame.transform.flip(self.image, False, True)
            if self.rect.top <= self.pos_inicial[1] and self.direcao.y == -1:
                self.direcao.y = 1
                self.rect.top = self.pos_inicial[1]
                pygame.transform.flip(self.image, False, True)

    def update(self, dt):
        self.old_rect = self.rect.copy()

        self.rect.topleft += self.direcao * self.Vel * dt
        self.check_borda()


