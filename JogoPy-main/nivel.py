import pygame.sprite

from config import *
from sprites import Sprite, Plataforma_Movel, DanoReset, ObjParado, DanoContinuo
from jogador import Jogador
from groups import AllSprites
from os.path import join


class Nivel:
    def __init__(self, tmx_map, switch_stage):
        # Remover self.display_surface, já que vamos usar a game_surface da classe Game
        self.num_niveis = None
        self.level_finish_rect = None
        self.pressed_botao = None
        self.botao = None
        self.jogador2 = None
        self.jogador = None
        self.switch_stage = switch_stage
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semi_collision_sprites = pygame.sprite.Group()
        self.dano_sprites = pygame.sprite.Group()
        self.setup(tmx_map)

    def setup(self, tmx_map):

        # chao
        for x, y, surf in tmx_map.get_layer_by_name("Decoracao").tiles():
            Sprite((x * tamanho_bloco, y * tamanho_bloco), surf, (self.all_sprites, ))
        for x, y, surf in tmx_map.get_layer_by_name("Chao").tiles():
            Sprite((x * tamanho_bloco, y * tamanho_bloco), surf, (self.all_sprites, self.collision_sprites))


        # objetos


        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "player1":
                self.jogador = Jogador(pygame.image.load(join("tiled\\png\\chickenc.png")), (obj.x, obj.y),
                                       (self.all_sprites,),
                                       self.collision_sprites, self.semi_collision_sprites,
                                       pygame.K_d, pygame.K_a, pygame.K_s, pygame.K_w)

        for obj in tmx_map.get_layer_by_name("Player"):
            if obj.name == "player2":
                self.jogador2 = Jogador(pygame.image.load(join("tiled\\png\\penguin.png")), (obj.x, obj.y),
                                        (self.all_sprites,),
                                        self.collision_sprites, self.semi_collision_sprites,
                                        pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP)

        self.jogador.outro_jogador = self.jogador2
        self.jogador2.outro_jogador = self.jogador
        for obj in tmx_map.get_layer_by_name("ObjParado"):
            if obj.name == "bandeira":
                self.num_niveis = obj.properties["nivel"]
                self.level_finish_rect = ObjParado((obj.x, obj.y), (self.all_sprites),pygame.image.load(join("flag.png")))
            if obj.name == "danoparado":
                ObjParado((obj.x, obj.y), (self.all_sprites, self.dano_sprites), pygame.image.load(join("fireball.png")))

        """
        if tmx_map.get_layer_by_name("Obstaculo"):

            for obj in tmx_map.get_layer_by_name("Obstaculo"):

                if obj.name == "botao":
                    self.pressed_botao = obj.properties["pressed_botao"]
                    self.botao = pygame.FRect((obj.x, obj.y), (obj.width, obj.height))
        """
        for obj in tmx_map.get_layer_by_name("Dano"):
                groups = self.all_sprites

                if obj.name == "danoreset":
                    direcao_movi = obj.properties["direcao"]
                    vel = 30
                    nome = obj.properties["nome"]
                    if nome == "fireball":
                        surf = pygame.image.load(join("fireball.png"))
                    else:
                        pass # adicionar futuras imagens pras outras fases

                    if direcao_movi == "y":

                            pos_inicial = (obj.x, obj.y)
                            pos_final = (obj.x , obj.y + 100)
                            self.hit = DanoReset((self.all_sprites, self.dano_sprites),
                                                                 pos_inicial, pos_final, direcao_movi, vel, pygame.transform.rotate(surf, 270))

                    else:
                            pos_inicial = (obj.x, obj.y)
                            pos_final = (obj.x + 50, obj.y)
                            self.hit = DanoReset((self.all_sprites, self.dano_sprites),
                                                                pos_inicial,  pos_final,direcao_movi,vel, pygame.transform.flip(pygame.image.load(join("fireball.png")), False, False))
                if obj.name == "danocontinuo":
                    direcao_movi = obj.properties["direcao"]
                    vel = 30
                    nome = obj.properties["nome"]
                    if nome == "":
                        surf = pygame.image.load(join("fireball.png"))
                    else:
                        pass # adicionar futuras imagens pras outras fases
                    pass
                if obj.name == "danoparado":
                    nome = obj.properties["nome"]
                    if nome == "nome":
                        surf = pygame.image.load(join("fireball.png"))
                    else:
                        pass # adicionar futuras imagens pras outras fases

        # Plataformas
        for obj in tmx_map.get_layer_by_name("Plataformas"):
            if obj.name == "Local":
                # horizontal
                if obj.width > obj.height:
                    direcao_movi = "x"
                    pos_inicial = (obj.x, obj.y + obj.height / 2)
                    pos_final = (obj.x + obj.width, obj.y + obj.height / 2)

                # vertical
                else:

                    direcao_movi = "y"
                    pos_inicial = (obj.x + obj.width / 2, obj.y)
                    pos_final = (obj.x + obj.width / 2, obj.y + obj.height)
                vel = obj.properties["Vel"]
                Plataforma_Movel((self.all_sprites, self.semi_collision_sprites), pos_inicial, pos_final, direcao_movi, vel)

        # for obj in tmx_map.get_layer_by_name("Inimigos"):
        #    if obj.name == "Enemy":
        #        player((obj.x, obj.y), self.all_sprites, self.enemy_collision_sprites)

    def map_change(self, num_nivel):
        if self.jogador.hitbox_rect.colliderect(self.level_finish_rect) and self.jogador2.hitbox_rect.colliderect(
                self.level_finish_rect):
            #  num_nivel = 1 + num_nivel

            #  print(num_nivel)
            self.switch_stage(num_nivel)

    """
    def press_botao(self):
        if self.jogador.hitbox_rect.colliderect(self.botao) or self.jogador2.hitbox_rect.colliderect(self.botao):
            self.pressed_botao = True
    """
    def dano(self):
        for sprite in self.dano_sprites:
            if sprite.rect.colliderect(self.jogador2.hitbox_rect) or sprite.rect.colliderect(self.jogador.hitbox_rect):
                #self.hit = True
                self.jogador2.respawn()
                self.jogador.respawn()

    def run(self, dt):
        self.display_surface.fill("#72647d")

        self.all_sprites.update(dt)

        x = ((self.jogador.hitbox_rect.x + self.jogador2.hitbox_rect.x) / 2)
        y = ((self.jogador.hitbox_rect.y + self.jogador2.hitbox_rect.y) / 2)
        center = [x, y]
        self.all_sprites.draw(center)
        self.map_change(self.num_niveis)
       # self.press_botao()
        self.dano()
