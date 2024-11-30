import pygame.draw
from dask.array import left_shift

from settings import *
from pygame import Vector2
from pygments.styles.gh_dark import GRAY_3
from pygments.styles.lightbulb import COLORS

from settings import *

class Tool:
    def __init__(self, name, level):
        self.locked=True, self.name,self.level=name,level
        # stats
        self.digspeedplus=
        self.damageplus=


    def unlocktools(self):
        self.locked=False


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



    def input(self):
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_UP]:
            self.index -= 1
        if keys[pygame.K_DOWN]:
            self.index += 1
        if keys[pygame.K_SPACE]:
            if self.selected_index != None:
                selected_tool = self.tool[self.selected_index]
                current_tool = self.tool[self.index]
                self.tool[self.index] = selected_tool
                self.tool[self.selected_index] = current_tool
                self.selected_index = None
            else:
                self.selected_index = self.index


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

            icon_surf=self.icon_frames[tool.name]
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

    def display_main(self,dt):
        tool=self.tool[self.index]

        #main rect
        rect=pygame.FRect(self.main_rect.left + self.list_width,self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height)
        pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0, 12,0, 12,0)

        #display your image and item image
        #item 모습
        top_rect = pygame.FRect(rect.topleft,(rect.width,rect.height*0.4))
        pygame.draw.rect(self.display_surface, COLORS['red'],top_rect,0,0,0,12)

        tool_surf =self.tool_frames[tool.name]
        tool_rect = tool_surf.get_frect(center = top_rect.center)
        self.display_surface.blit(tool_surf,tool_rect)

        #name
        name_surf=self.fonts['bold'].render(tool.name,False,COLORS['white'])
        name_rect=name_surf.get_frect( topleft= top_rect.topleft+Vector2(10,10) )
        self.display_surface.blit(name_surf,name_rect)

        #level
        level_surf = self.fonts['regular'].render(f'level:{tool.level}', False, COLORS['white'])
        level_rect = level_surf.get_frect(topleft=top_rect.bottomleft+Vector2(10,-20))
        self.display_surface.blit(level_surf, level_rect)

        #level and how to use




    def update(self,dt):
        #input
        self.input()
        self.display_surface.blit(self.tint_surf,(0,0))
        # pygame.draw.rect(self.display_surface,'black',self.main_rect)

        #tint the main game
        #display the list
        self.display_list()
        self.display_main(dt)

