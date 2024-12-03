import pygame.draw
from pygame import Vector2
from game_data import *
from settings import *
from support import *

#장비 클래스 삽이랑 총 자동차는 모르겠음
class Tool:
    def __init__(self, name, level):
        self.locked=True
        self.name,self.level=name,level
        # stats
        self.digspeed=TOOL_DATA[name]['level'][level]['digspeed']
        self.plusdamage=TOOL_DATA[name]['level'][level]['plusdamage']
        self.skill=TOOL_DATA[name]['level'][level]['skill']
        self.stat=[self.plusdamage,self.digspeed,self.skill]
        self.guide=TOOL_DATA[name]['guide'][level]

    def unlock_skill(self):
        if self.level>=5:
            self.locked=False

    def tool_level_up(self,name):
        self.level+=1
        self.unlock_skill()
        # stats
        self.digspeed = TOOL_DATA[name]['level'][self.level]['digspeed']
        self.plusdamage = TOOL_DATA[name]['level'][self.level]['plusdamage']
        self.skill = TOOL_DATA[name]['level'][self.level]['skill']
        self.guide = TOOL_DATA[name]['guide'][self.level]
        self.stat = [self.plusdamage, self.digspeed, self.skill]

class Item:
    def __init__(self,name):
        self.name=name
        self.cost=ITEM_DATA[self.name]['cost']
        self.guide=ITEM_DATA[self.name]['guide']
    def item_effect(self,player):
        self.player=player



class ToolIndex:
    def __init__(self,tool,fonts,tool_frames):
        self.display_surface=pygame.display.get_surface()
        self.fonts=fonts
        self.tool=tool

        #frames
        self.icon_frames =tool_frames['icons']
        self.tool_frames=tool_frames['icons'] #나중에 더 간지나는 큰 이미지 추가하기

        #tint surf
        self.tint_surf =pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)

        self.main_rect = pygame.FRect(0,0,WINDOW_WIDTH*0.6, WINDOW_HEIGHT*0.8).move_to(center=(WINDOW_WIDTH/2,WINDOW_HEIGHT/2))

        #list
        self.visible_items=6
        self.list_width =self.main_rect.width*0.3
        self.item_height =self.main_rect.height/self.visible_items
        self.index=0
        self.selected_index = None
        self.selected_tool =None


    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_w]:
            self.index -= 1
        if keys[pygame.K_s]:
            self.index += 1
        if keys[pygame.K_SPACE]:
            if self.selected_index != None:
                if self.index==self.selected_index:
                    self.selected_index=None
                    self.selected_tool = None
                else:
                    self.selected_index=self.index
                    self.selected_tool = self.tool[self.selected_index]
            else:
                self.selected_index = self.index
                self.selected_tool = self.tool[self.selected_index]


    def display_list(self):
        v_offset = 0 if self.index<self.visible_items else (self.index - self.visible_items)*self.item_height
        for index,tool in self.tool.items():
            #colors
            bg_color=COLORS['gray']  if self.index !=index else COLORS['light']
            text_color=COLORS['white'] if self.selected_index !=index else COLORS['gold']


            top = self.main_rect.top+index*self.item_height
            item_rect = pygame.FRect(self.main_rect.left,top,self.list_width,self.item_height)


            text_surf=self.fonts['regular'].render(tool.name,False,text_color)
            text_rect=text_surf.get_frect(midleft=item_rect.midleft+Vector2(130,0))

            icon_surf=smallerimage2(self.icon_frames[tool.name])
            icon_rect=icon_surf.get_frect(center=item_rect.midleft+Vector2(50,0))

            if item_rect.colliderect(self.main_rect):

                #check corner

                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect,0,0,12)
                elif item_rect.collidepoint(self.main_rect.bottomleft+Vector2(1,-1)):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0,0,0, 12,0)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)



                self.display_surface.blit(text_surf,text_rect)
                self.display_surface.blit(icon_surf,icon_rect)

        for i in range(min(self.visible_items,len(self.tool))):
            y=self.main_rect.top +self.item_height*i
            left=self.main_rect.left
            right=self.main_rect.left+self.list_width
            pygame.draw.line(self.display_surface, COLORS['light-gray'],(left,y),(right,y))
        shadow_surf=pygame.Surface((4,self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf,(self.main_rect.left+self.list_width-4,self.main_rect.top))

    def display_main(self):
        tool=self.tool[self.index]

        #main rect

        rect=pygame.FRect(self.main_rect.left + self.list_width,self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height)
        surf=pygame.Surface((rect.width,rect.height))
        surf.set_alpha(200)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0, 12,0, 12,0)

        #display your image and item image
        #item 모습
        top_rect = pygame.FRect(rect.topleft,(rect.width,rect.height*0.3))
        pygame.draw.rect(self.display_surface, COLORS['red'],top_rect,0,0,0,12)

        tool_surf =self.tool_frames[tool.name]
        tool_rect = tool_surf.get_frect(center = top_rect.center)
        self.display_surface.blit(tool_surf,tool_rect)

        #name
        name_surf=self.fonts['bold'].render(tool.name,False,COLORS['white'])
        name_rect=name_surf.get_frect( topleft= top_rect.topleft+Vector2(10,10) )
        self.display_surface.blit(name_surf,name_rect)

        #level
        level_surf = self.fonts['regular'].render(f'level: {tool.level}/10', False, COLORS['white'])
        level_rect = level_surf.get_frect(topleft=top_rect.bottomleft+Vector2(10,-20))
        self.display_surface.blit(level_surf, level_rect)
        draw_bar(
            surface=self.display_surface,
            rect=pygame.FRect(0,0,400,30).move_to(center=top_rect.midbottom+Vector2(-20,20)),
            value=tool.level,
            max_value=10,
            color=COLORS['white'],
            bg_color=COLORS['black']
        )
        level1_surf = self.fonts['regular'].render(f'max \nlevel', False, COLORS['gold'])
        level1_rect = level1_surf.get_frect(topleft=top_rect.midbottom + Vector2(200, 0))
        self.display_surface.blit(level1_surf, level1_rect)




        #ablility and skill
        for i in range(len(tool.stat)):
            draw_text_in_box(
                surface=self.display_surface,
                rect=pygame.FRect(0,0,200,40).move_to(midbottom=rect.midbottom+Vector2(0,-40*i-10)),
                bg_color=COLORS['white'],
                txt_surf=self.fonts['regular'].render(f'{tool.stat[i]}', False, COLORS['black']),
                )


        #how to use
        guide_surf = self.fonts['explain'].render(tool.guide, False, COLORS['white'])
        guide_rect = level_surf.get_frect(topleft=top_rect.bottomleft + Vector2(0, 80))
        self.display_surface.blit(guide_surf, guide_rect)
        #쓸 수 없는 아이템
        if tool.level==0:
            self.display_surface.blit(surf,rect.topleft)


    def update(self,dt):
        #input
        self.input()
        self.display_surface.blit(self.tint_surf,(0,0))
        # pygame.draw.rect(self.display_surface,'black',self.main_rect)

        #tint the main game
        #display the list
        self.display_list()
        self.display_main()



class TrainingIndex:
    def __init__(self,fonts,player,tool,item_frames,tool_frames):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.place = None
        self.player = player
        self.item={(0,0):Item('HP_potion'), (0,1):Item('XP_potion'), (0,2):Item('THIRST_potion'),(0,3):Item('THIRST_potion'),(0,4):Item('THIRST_potion'),
                   (1, 0): Item('HP_potion'), (1, 1): Item('XP_potion'), (1, 2): Item('THIRST_potion'),(1, 3): Item('THIRST_potion'), (1, 4):Item('THIRST_potion'),
                   (2, 0): Item('HP_potion'), (2, 1): Item('XP_potion'), (2, 2): Item('THIRST_potion'),(2, 3): Item('THIRST_potion'), (2, 4): Item('THIRST_potion')
                   }
        self.tool=tool
        self.item_frames=item_frames
        self.tool_frames=tool_frames
        # tint surf
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_surf.set_alpha(200)
        self.visible_items=6

        self.main_rect = pygame.FRect(0, 0, WINDOW_WIDTH * 0.6, WINDOW_HEIGHT * 0.8).move_to(
            center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        self.list_width=0.2*self.main_rect.width
        self.item_height=self.list_width
        self.list_width2 = self.main_rect.width * 0.3
        self.item_height2 = self.main_rect.height / self.visible_items

        self.index1=[0,0]
        self.index2=0

        self.selected_index1=None
        self.selected_index2=None

        self.selected_item=None
        self.selected_tool=None

        self.is_pressed=False

    def input1(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_w]:
            self.index1[0] -= 1
        if keys[pygame.K_s]:
            self.index1[0] += 1
        if keys[pygame.K_a]:
            self.index1[1] -= 1
        if keys[pygame.K_d]:
            self.index1[1] += 1
        if keys[pygame.K_SPACE]:
            if self.selected_index1 != None:
                if self.index1==self.selected_index1:
                    self.selected_index1=None
                    self.selected_item = None
                else:
                    self.selected_index1 =self.index1
                    self.selected_item = self.item[tuple(self.selected_index1)]
            else:
                self.selected_index1 = self.index1
                self.selected_item = self.item[tuple(self.selected_index1)]



    def display_list1(self):

        top_rect = pygame.FRect(self.main_rect.topleft, (self.main_rect.width, 100))
        pygame.draw.rect(self.display_surface, COLORS['red'], top_rect, 0, 12)

        shop_surf=self.fonts['bold'].render('shop', False, COLORS['white'])
        shop_rect=shop_surf.get_frect(center=self.main_rect.midtop+Vector2(0,50))
        self.display_surface.blit(shop_surf, shop_rect)

        for index,item in self.item.items():
            #colors
            index=list(index)

            bg_color=COLORS['light']  if self.index1==index else COLORS['gray'] if (index[0]+index[1])%2==0 else COLORS['dark']
            text_color=COLORS['white'] if self.selected_index1 !=index or self.selected_index1==None else COLORS['gold']

            top = self.main_rect.top+index[0]*self.item_height+100
            left= self.main_rect.left+index[1]*self.list_width
            item_rect = pygame.FRect(left,top,self.list_width,self.item_height)

            text_surf=self.fonts['regular'].render(item.name,False,text_color)
            text_rect=text_surf.get_frect(midbottom=item_rect.midbottom+Vector2(0,-10))

            icon_surf=smallerimage2(self.item_frames[item.name])
            icon_rect=icon_surf.get_frect(center=item_rect.center)

            pygame.draw.rect(self.display_surface, bg_color, item_rect,0,12,12,12,12,12)
            self.display_surface.blit(text_surf,text_rect)
            self.display_surface.blit(icon_surf,icon_rect)

        self.display_surface.blit(text_surf, text_rect)
        self.display_surface.blit(icon_surf, icon_rect)

        if self.selected_index1:
            rect=pygame.FRect(0, 0, WINDOW_WIDTH * 0.4, WINDOW_HEIGHT * 0.3).move_to(midbottom=self.main_rect.midbottom+Vector2(0,-WINDOW_HEIGHT * 0.1))
            text_surf = self.fonts['regular'].render(self.item[tuple(self.selected_index1)].guide, False, COLORS['white'])
            text_rect = text_surf.get_frect(center=rect.center+Vector2(0,-WINDOW_HEIGHT * 0.1))
            pygame.draw.rect(self.display_surface,COLORS['water'],rect,0,6)
            self.display_surface.blit(text_surf,text_rect)

    def click1(self,event):
        if self.selected_index1:
            name = self.item[tuple(self.selected_index1)].name
            buy_rect = pygame.FRect(0, 0, 300, 80).move_to(midbottom=self.main_rect.midbottom + Vector2(0, -100))
            bg_rect = buy_rect.copy()
            txt_surf = self.fonts['explain'].render(f'BUY', False, COLORS['white'])
            txt_rect = txt_surf.get_frect(center=bg_rect.center)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if buy_rect.collidepoint(event.pos):  # 마우스가 Rect 안에 있을 때
                    self.is_pressed=True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.is_pressed:
                    self.is_pressed=False

                if name=='HP_potion':
                    self.player.hp+=50
                elif name=='XP_potion':
                    self.player.xp+=200
                elif name=='THIRST_potion':
                    self.player.thirst+=20
                    # 눌린 상태였다면

    def button1(self):
        if self.selected_index1:
            buy_rect = pygame.FRect(0, 0, 300, 80).move_to(midbottom=self.main_rect.midbottom + Vector2(0, -100))
            bg_rect = buy_rect.copy()
            txt_surf = self.fonts['explain'].render(f'BUY', False, COLORS['white'])
            txt_rect = txt_surf.get_frect(center=bg_rect.center)
            if self.is_pressed:
                pygame.draw.rect(self.display_surface, COLORS['gray'], buy_rect, 0, 12)
                self.display_surface.blit(txt_surf, txt_rect)
            else:
                pygame.draw.rect(self.display_surface, COLORS['light'], buy_rect, 0, 12)
                self.display_surface.blit(txt_surf, txt_rect)
    def input2(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_w]:
            self.index2 -= 1
        if keys[pygame.K_s]:
            self.index2 += 1
        if keys[pygame.K_SPACE]:
            if self.selected_index2 != None:
                if self.index2 == self.selected_index2:
                    self.selected_index2 = None
                    self.selected_tool = None
                else:
                    self.selected_index2 = self.index2
                    self.selected_tool = self.tool[self.selected_index2]
            else:
                self.selected_index2 = self.index2
                self.selected_tool = self.tool[self.selected_index2]

    def display_list2(self):
        v_offset = 0 if self.index2 < self.visible_items else (self.index2 - self.visible_items) * self.item_height2
        for index, tool in self.tool.items():
            # colors
            bg_color = COLORS['gray'] if self.index2 != index else COLORS['light']
            text_color = COLORS['white'] if self.selected_index2 != index  else COLORS['gold']

            top = self.main_rect.top + index * self.item_height2
            item_rect = pygame.FRect(self.main_rect.left, top, self.list_width2, self.item_height2)

            text_surf = self.fonts['regular'].render(tool.name, False, text_color)
            text_rect = text_surf.get_frect(midleft=item_rect.midleft + Vector2(130, 0))

            icon_surf = smallerimage2(self.tool_frames[tool.name])
            icon_rect = icon_surf.get_frect(center=item_rect.midleft + Vector2(50, 0))

            if item_rect.colliderect(self.main_rect):

                # check corner

                if item_rect.collidepoint(self.main_rect.topleft):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 12)
                elif item_rect.collidepoint(self.main_rect.bottomleft + Vector2(1, -1)):
                    pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 0, 0, 12, 0)
                else:
                    pygame.draw.rect(self.display_surface, bg_color, item_rect)

                self.display_surface.blit(text_surf, text_rect)
                self.display_surface.blit(icon_surf, icon_rect)

        for i in range(min(self.visible_items, len(self.tool))):
            y = self.main_rect.top + self.item_height2 * i
            left = self.main_rect.left
            right = self.main_rect.left + self.list_width
            pygame.draw.line(self.display_surface, COLORS['light-gray'], (left, y), (right, y))
        shadow_surf = pygame.Surface((4, self.main_rect.height))
        shadow_surf.set_alpha(100)
        self.display_surface.blit(shadow_surf, (self.main_rect.left + self.list_width2 - 4, self.main_rect.top))




    def display_main2(self):
        tool=self.tool[self.index2]

        #main rect

        rect=pygame.FRect(self.main_rect.left + self.list_width2,self.main_rect.top, self.main_rect.width - self.list_width2, self.main_rect.height)
        surf=pygame.Surface((rect.width,rect.height))
        surf.set_alpha(200)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0, 12,0, 12,0)

        #display your image and item image
        #item 모습
        top_rect = pygame.FRect(rect.topleft,(rect.width,rect.height*0.3))
        pygame.draw.rect(self.display_surface, COLORS['red'],top_rect,0,0,0,12)

        tool_surf =self.tool_frames[tool.name]
        tool_rect = tool_surf.get_frect(center = top_rect.center)
        self.display_surface.blit(tool_surf,tool_rect)

        #name
        name_surf=self.fonts['bold'].render(tool.name,False,COLORS['white'])
        name_rect=name_surf.get_frect( topleft= top_rect.topleft+Vector2(10,10) )
        self.display_surface.blit(name_surf,name_rect)


        draw_bar(
            surface=self.display_surface,
            rect=pygame.FRect(0,0,400,30).move_to(center=top_rect.midbottom+Vector2(-20,20)),
            value=tool.level,
            max_value=10,
            color=COLORS['white'],
            bg_color=COLORS['black']
        )
        level1_surf = self.fonts['regular'].render(f'max \nlevel', False, COLORS['gold'])
        level1_rect = level1_surf.get_frect(topleft=top_rect.midbottom + Vector2(200, 0))
        self.display_surface.blit(level1_surf, level1_rect)

        # level
        level_surf = self.fonts['explain'].render(f'level: {tool.level}/10', False, COLORS['white'])
        level_rect = level_surf.get_frect(midtop=top_rect.midbottom + Vector2(0, 60))
        self.display_surface.blit(level_surf, level_rect)

        # draw_text_in_box(surface=self.display_surface,
        #                  rect=pygame.FRect(0,0,300,80).move_to(midbottom=self.main_rect.midbottom+Vector2(0, -200)),
        #                  bg_color=COLORS['light'],
        #                  txt_surf=self.fonts['explain'].render(f'UPGRADE', False, COLORS['gold']),
        #                  radius=12)

    def click2(self,event):

        upgrade_rect = pygame.FRect(0, 0, 300, 80).move_to(midbottom=self.main_rect.midbottom+Vector2(0, -200))
        bg_rect=upgrade_rect.copy()
        txt_surf = self.fonts['explain'].render(f'UPGRADE', False, COLORS['gold'])
        txt_rect = txt_surf.get_frect(center=bg_rect.center)



        if event.type == pygame.MOUSEBUTTONDOWN:
            if upgrade_rect.collidepoint(event.pos):  # 마우스가 Rect 안에 있을 때
                self.is_pressed=True
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.is_pressed:
                self.is_pressed=False
                self.player.tool[self.index2].level+=1
                # 눌린 상태였다면

    def button2(self):
        upgrade_rect = pygame.FRect(0, 0, 300, 80).move_to(midbottom=self.main_rect.midbottom + Vector2(self.main_rect.width/2*0.3, -200))
        bg_rect = upgrade_rect.copy()
        txt_surf = self.fonts['explain'].render(f'UPGRADE', False, COLORS['gold'])
        txt_rect = txt_surf.get_frect(center=bg_rect.center)
        if self.is_pressed:
            pygame.draw.rect(self.display_surface, COLORS['gray'], upgrade_rect, 0, 12)
            self.display_surface.blit(txt_surf, txt_rect)
        else:
            pygame.draw.rect(self.display_surface, COLORS['light'], upgrade_rect, 0, 12)
            self.display_surface.blit(txt_surf, txt_rect)



    def update(self):
        self.display_surface.blit(self.tint_surf, (0, 0))
        if self.place=='Shop':
            self.input1()
            self.display_list1()
            self.button1()
        if self.place=='Training':
            self.input2()
            self.display_list2()
            self.display_main2()
            self.button2()