import pygame
import math
import os
from settings import PATH
from settings import PATH_Right   #右邊的路徑
pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

class Enemy():
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = PATH
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        #利用enemy現在的位置來設定血條的位置，第一條是紅色部分，第二條是綠色部分
        pygame.draw.rect(win, [255,0,0], [self.x-15, self.y-30, self.max_health*3, 5]) 
        pygame.draw.rect(win, [0,255,0], [self.x-15, self.y-30, self.health*3, 5])

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        # 將現在的path上的座標點儲存，並計算出兩點距離需要走多少步
        ax, ay = self.path[self.path_pos] 
        bx, by = self.path[self.path_pos+1]
        distance = math.sqrt((ax - bx)**2 + (ay - by)**2)
        max_count = int(distance / self.stride)
        #當移動的步數小於到達下一個點的步數時，算出到下一個點走一步需要移動多少x,y座標
        if self.move_count < max_count:
            unit_vector_x = (bx - ax) / distance
            unit_vector_y = (by - ay) / distance
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride
            # 更新座標並增加count所記的步數
            self.x += delta_x
            self.y += delta_y
            self.move_count += 1
        #當移動的步數大於等於到達下一個點的步數時，將座標點改為下一個座標，並將count歸 0
        else:
            self.path_pos+=1
            self.move_count=0


class EnemyGroup:
    def __init__(self):
        self.gen_count = 0
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = [Enemy()]  # don't change this line until you do the EX.3 
        self.wave_count=0    #用來計算第幾波敵人
        
    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # Hint: self.expedition.append(self.reserved_members.pop())
        # 在reserved_members不是空的時候才會執行
        if  not self.is_empty():
            if self.gen_count==self.gen_period:      #每經過120會將reserved_members裡的enemy放進expedition，使其開始行軍
                self.expedition.append(self.reserved_members.pop())
                self.gen_count=0
            else:
                self.gen_count+=1                    #計算fps
        
    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        #根據輸入的num來把敵人的數量放進reserved_members
        for i in range(0,num):
            i=Enemy()    #設定 i為Enemy的物件
            if self.wave_count%2==1:     #當 wave次數為偶數時將Enemy的路徑設為右邊的路
                i.path=PATH_Right
                i.x, i.y = i.path[0]
            self.reserved_members.append(i)
            
        self.wave_count+=1    #計算 wave次
            
    
    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)




