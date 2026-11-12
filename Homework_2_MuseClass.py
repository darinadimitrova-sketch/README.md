import random
from muse import MuseClass


class ClericClass(MuseClass):
    def __init__(self, name, min_damage, max_damage):
        MuseClass.__init__(self, name, min_damage, max_damage)
        self.heal_ready = 1
        self.mana_ready = 1
        self.attack_ready = 1
        self.defense_ready = 1
        self.critical_ready = 1
        self.attack_end = 0
        self.defense_end = 0
        self.critical_end = 0

    def use_greater_heal(self):
        if self.round_number >= self.heal_ready:
            self.heal(1000 * 0.35)
            self.heal_ready = self.round_number + 7
            print(self.name, "uses Greater Heal for 350 HP")
            return True
        else:
            print("Greater Heal is on cooldown")
            return False

    def use_mana_restore(self):
        if self.round_number >= self.mana_ready:
            self.mana = self.mana + 500 * 0.65

            if self.mana > 500:
                self.mana = 500

            self.mana_ready = self.round_number + 5
            print(self.name, "uses Mana Restore for 325 MP")
            return True
        else:
            print("Mana Restore is on cooldown")
            return False

    def use_attack_up(self):
        if self.round_number >= self.attack_ready:
            self.attack_end = self.round_number + 3
            self.attack_ready = self.round_number + 5
            print(self.name, "increases attack by 40% for 3 rounds")
            return True
        else:
            print("Attack Up is not ready")
            return False

    def use_defense_up(self):
        if self.round_number >= self.defense_ready:
            self.defense_end = self.round_number + 3
            self.defense_ready = self.round_number + 5
            print(self.name, "increases defense for 3 rounds")
            return True
        else:
            print("Defense Up is not ready")
            return False

    def use_critical_hit_enhance(self):
        if self.round_number >= self.critical_ready:
            self.critical_end = self.round_number + 3
            self.critical_ready = self.round_number + 5
            print(self.name, "has a 25% critical hit chance for 3 rounds")
            return True
        else:
            print("Critical Hit Enhance is not ready")
            return False

    def attack(self, enemy):
        damage = random.randint(self.min_damage, self.max_damage)

        if self.round_number < self.attack_end:
            damage = damage * 1.40

        if self.round_number < self.critical_end:
            if random.randint(1, 4) == 1:
                damage = damage * 2
                print("Critical hit!")

        enemy.take_damage(damage)
        print(self.name, "attacks for", round(damage, 2), "damage")

    def take_damage(self, damage):
        if self.round_number < self.defense_end:
            damage = damage * 0.72

        self.health = self.health - damage

        if self.health < 0:
            self.health = 0
