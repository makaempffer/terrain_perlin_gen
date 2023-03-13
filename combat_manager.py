from combat_system import CombatSystem
from settings import *
from pop_menu import PopMenu
class CombatManager:
    def __init__(self, screen, npc_group: pg.sprite.Group, 
                player_group: pg.sprite.Group, 
                menu: PopMenu,
                combatSystem: CombatSystem = CombatSystem):
        self.menu = menu
        self.screen = screen
        self.combat_system = combatSystem
        self.npc_group = npc_group
        self.player_group = player_group
        self.closest_ref = None
        self.closest_possible = 10000
        self.player_ref = None
        

    def get_player_vs_npc(self, player= None):
        player_ref = player
        for player in self.player_group:
            player_ref = player
            player_x = player.rect.x
            player_y = player.rect.y
            self.player_ref = player_ref
        for npc in self.npc_group:
            npc_x, npc_y = npc.rect.x, npc.rect.y
            dist_x = abs(player_x - npc_x)
            dist_y = abs(player_y - npc_y)
            avg_dist = (dist_x + dist_y) / 2

            if avg_dist < player_ref.vision_distance:
                if  avg_dist < self.closest_possible:
                    self.closest_possible = avg_dist
                    self.closest_ref = npc
            if self.closest_ref:
                player_to_closest_x = player_x - self.closest_ref.rect.x
                player_to_closest_y = player_y - self.closest_ref.rect.y
                player_to_closest_avg = (player_to_closest_x + player_to_closest_y) / 2
                #print(player_to_closest_avg)

                if player_to_closest_avg < player_ref.vision_distance:
                    pg.draw.rect(self.screen, (230, 20, 20), self.closest_ref.rect)
                    #pg.draw.rect(self.screen, (20, 230, 20), npc.rect)
        
        self.closest_possible = 10000

    def create_battle(self, a, b):
        self.combat_system.create_battle_instance(self, a, b)
        
    
    def player_create_instance(self):
        npc_objective = self.menu.npcTarget
        if npc_objective != None:
            action = self.menu.previous_action
        
            if action == "Attack":
                self.create_battle(self.player_ref, self.closest_ref)
        

    def update(self):
        self.get_player_vs_npc()
        self.player_create_instance()