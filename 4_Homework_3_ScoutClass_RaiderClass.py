import random


import random




class CharacterClass:
    def __init__(self, name, min_damage, max_damage):
        self.name = name
        self.health = 1000
        self.mana = 500
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.skip_rounds = 0
        self.fire_rounds = 0
        self.bleed_rounds = 0
        self.arrow_poison_rounds = 0
        self.knife_poison_rounds = 0
        self.reflect_percent = 0
        self.round_number = 1

    def take_damage(self, damage):
        old_health = self.health
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0
        return old_health - self.health

    def hit_enemy(self, enemy, damage):
        actual_damage = enemy.take_damage(damage)
        if enemy.reflect_percent > 0:
            reflected = actual_damage * enemy.reflect_percent / 100
            enemy.reflect_percent = 0
            if self.is_alive():
                self.take_damage(reflected)
                print(enemy.name, "reflects", round(reflected, 2), "damage")

    def attack(self, enemy):
        damage = random.randint(self.min_damage, self.max_damage)
        self.hit_enemy(enemy, damage)
        print(self.name, "attacks for", round(damage, 2), "damage")

    def heal(self, amount):
        self.health = self.health + amount
        if self.health > 1000:
            self.health = 1000

    def is_alive(self):
        return self.health > 0



class MuseClass(CharacterClass):
    pass



class SoldierClass(CharacterClass):
    pass



class DealerClass(CharacterClass):
    def use_gun(self, enemy):
        damage = enemy.health * 0.55
        self.hit_enemy(enemy, damage)
        print(self.name, "uses gun for", round(damage, 2), "damage")

        chance = random.randint(1, 5)
        if chance == 1 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 2
            print(enemy.name, "must skip 2 turns")



class HawkerClass(CharacterClass):
    def use_stealth(self):
        mana_cost = 2 * 10
        if self.mana >= mana_cost:
            self.mana = self.mana - mana_cost
            print(self.name, "uses stealth and spends", mana_cost, "MP")
            return True
        else:
            print(self.name, "does not have enough mana")
            return False

    def use_bow(self, enemy):
        damage = enemy.health * 0.35
        self.hit_enemy(enemy, damage)
        print(self.name, "uses bow for", round(damage, 2), "damage")

        chance = random.randint(1, 3)
        if chance == 1 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")



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
            old_health = self.health
            self.heal(1000 * 0.35)
            restored = self.health - old_health
            self.heal_ready = self.round_number + 7
            print(self.name, "uses Greater Heal and restores", round(restored, 2), "HP")
            return True
        else:
            print("Greater Heal is on cooldown")
            return False

    def use_mana_restore(self):
        if self.round_number >= self.mana_ready:
            old_mana = self.mana
            self.mana = self.mana + 500 * 0.65
            if self.mana > 500:
                self.mana = 500
            restored = self.mana - old_mana
            self.mana_ready = self.round_number + 5
            print(self.name, "uses Mana Restore and restores", round(restored, 2), "MP")
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
            print(self.name, "increases defense by 28% for 3 rounds")
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

        self.hit_enemy(enemy, damage)
        print(self.name, "attacks for", round(damage, 2), "damage")

    def take_damage(self, damage):
        if self.round_number < self.defense_end:
            damage = damage * 0.72
        return CharacterClass.take_damage(self, damage)



class MageClass(MuseClass):
    def __init__(self, name, min_damage, max_damage):
        MuseClass.__init__(self, name, min_damage, max_damage)
        self.quick_cast_ready = 1

    def use_fireball(self, enemy):
        damage = random.randint(50, 80)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Fireball for", damage, "damage")

        if enemy.is_alive():
            enemy.fire_rounds = 3
            print(enemy.name, "will take fire damage for 3 rounds")

    def use_ice_ball(self, enemy):
        damage = random.randint(30, 50)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Ice Ball for", damage, "damage")

        chance = random.randint(1, 100)
        if chance <= 15 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")

    def use_lightning_ball(self, enemy):
        damage = random.randint(60, 70)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Lightning Ball for", damage, "damage")

        chance = random.randint(1, 100)
        if chance <= 5 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")

    def use_quick_cast(self):
        if self.round_number >= self.quick_cast_ready:
            self.quick_cast_ready = self.round_number + 7
            print(self.name, "can use two spells this turn")
            return True
        else:
            print("Quick Cast is on cooldown")
            return False



class KnightClass(SoldierClass):
    def __init__(self, name, min_damage, max_damage):
        SoldierClass.__init__(self, name, min_damage, max_damage)
        self.defense_end = 0
        self.defense_ready = 1

    def use_enhance_defence(self):
        if self.round_number >= self.defense_ready:
            self.defense_end = self.round_number + 3
            self.defense_ready = self.round_number + 7
            print(self.name, "increases defense by 70% for 3 rounds and loses this action")
            return True
        else:
            print("Enhance Defence is on cooldown")
            return False

    def use_shield_reflect(self):
        chance = random.randint(1, 100)
        if chance <= 5:
            self.reflect_percent = 70
        elif chance <= 20:
            self.reflect_percent = 40
        elif chance <= 50:
            self.reflect_percent = 20
        else:
            self.reflect_percent = 5
        print(self.name, "reflects", self.reflect_percent, "% of the next attack")

    def use_impact_wave(self, enemy):
        damage = random.randint(80, 100)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Impact Wave for", damage, "damage")

    def use_shield_slam(self, enemy):
        damage = random.randint(70, 90)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Shield Slam for", damage, "damage")
        if random.randint(1, 100) <= 8 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")

    def use_one_hand_attack(self, enemy):
        damage = random.randint(40, 70)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses One Hand Attack for", damage, "damage")

    def take_damage(self, damage):
        if self.round_number < self.defense_end:
            damage = damage * 0.30
        return CharacterClass.take_damage(self, damage)



class ChampionClass(SoldierClass):
    def __init__(self, name, min_damage, max_damage):
        SoldierClass.__init__(self, name, min_damage, max_damage)
        self.berserk_end = 0
        self.berserk_ready = 1
        self.blood_ready = 1

    def use_berserk(self):
        if self.round_number >= self.berserk_ready:
            chance = random.randint(1, 100)
            if chance <= 3:
                duration = 6
            elif chance <= 10:
                duration = 5
            elif chance <= 40:
                duration = 4
            elif chance <= 65:
                duration = 3
            else:
                duration = 2
            self.health = self.health - 100
            if self.health < 0:
                self.health = 0
            self.berserk_end = self.round_number + duration
            self.berserk_ready = self.round_number + 7
            print(self.name, "uses Berserk for", duration, "rounds and loses 100 HP")
            return True
        else:
            print("Berserk is on cooldown")
            return False

    def use_blood_attack(self, enemy):
        if self.round_number >= self.blood_ready:
            damage = enemy.health * 0.15
            old_health = enemy.health
            CharacterClass.hit_enemy(self, enemy, damage)
            self.heal(old_health - enemy.health)
            self.blood_ready = self.round_number + 3
            print(self.name, "steals", round(damage, 2), "HP")
            return True
        else:
            print("Blood Attack is on cooldown")
            return False

    def use_piercing_stab(self, enemy):
        damage = random.randint(50, 80)
        self.hit_enemy(enemy, damage)
        if enemy.is_alive():
            enemy.bleed_rounds = 5
        print(self.name, "uses Piercing Stab for", damage, "damage")

    def use_leap_strike(self, enemy):
        damage = random.randint(70, 90)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Leap Strike for", damage, "damage")

    def hit_enemy(self, enemy, damage):
        if self.round_number < self.berserk_end:
            damage = damage * 1.70
        CharacterClass.hit_enemy(self, enemy, damage)

class ScoutClass(HawkerClass):
    def __init__(self, name, min_damage, max_damage):
        HawkerClass.__init__(self, name, min_damage, max_damage)
        self.speed_ready = 1

    def use_tripple_shot(self, enemy):
        first = random.randint(50, 80)
        second = first * 0.85
        third = second * 0.85
        damage = first + second + third
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Tripple Shot for", round(damage, 2), "damage")

    def use_eagle_shot(self, enemy):
        damage = random.randint(50, 90)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Eagle Shot for", damage, "damage")
        if random.randint(1, 100) <= 35 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")

    def use_speed_shot(self):
        if self.round_number >= self.speed_ready:
            self.speed_ready = self.round_number + 7
            print(self.name, "can use two shots this round")
            return True
        else:
            print("Speed Shot is on cooldown")
            return False

    def use_poison_arrow(self, enemy):
        damage = random.randint(40, 80)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Poison Arrow for", damage, "damage")
        if enemy.is_alive():
            enemy.arrow_poison_rounds = 6
            print(enemy.name, "will take 5 poison damage for 6 rounds")


class RaiderClass(HawkerClass):
    def __init__(self, name, min_damage, max_damage):
        HawkerClass.__init__(self, name, min_damage, max_damage)
        self.camouflage_rounds = 0
        self.hidden_attack = False
        self.next_attack_bonus = False
        self.mana_blood_ready = 1

    def hit_enemy(self, enemy, damage):
        if self.next_attack_bonus == True:
            damage = damage * 1.20
            self.next_attack_bonus = False
            print(self.name, "gets 20% extra damage")
        CharacterClass.hit_enemy(self, enemy, damage)

    def use_double_slash(self, enemy):
        first = random.randint(40, 50)
        second = first * 1.15
        damage = first + second
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Double Slash for", round(damage, 2), "damage")

    def use_camouflage(self):
        chance = random.randint(1, 100)
        if chance <= 30:
            self.camouflage_rounds = 4
        elif chance <= 70:
            self.camouflage_rounds = 3
        elif chance <= 90:
            self.camouflage_rounds = 2
        else:
            self.camouflage_rounds = 0
        print(self.name, "uses Camouflage for", self.camouflage_rounds, "rounds")

    def use_screw_attack(self, enemy):
        damage = random.randint(70, 90)
        self.hit_enemy(enemy, damage)
        self.next_attack_bonus = True
        print(self.name, "uses Screw Attack for", damage, "damage")
        print("The next attack gets 20% extra damage")

    def use_posion_knife(self, enemy):
        damage = random.randint(40, 80)
        self.hit_enemy(enemy, damage)
        print(self.name, "uses Posion Knife for", damage, "damage")
        if enemy.is_alive():
            enemy.knife_poison_rounds = 6
            print(enemy.name, "will take 8 poison damage for 6 rounds")

    def use_mana_blood(self, enemy):
        if self.round_number >= self.mana_blood_ready:
            damage = enemy.health * 0.15
            mana_gain = enemy.health * 0.10
            health_gain = enemy.health * 0.05
            CharacterClass.hit_enemy(self, enemy, damage)
            self.mana = self.mana + mana_gain
            if self.mana > 500:
                self.mana = 500
            self.heal(health_gain)
            self.mana_blood_ready = self.round_number + 3
            print(self.name, "uses Mana Blood and steals", round(damage, 2), "HP")
            return True
        else:
            print("Mana Blood is on cooldown")
            return False

def create_character(choice):
    if choice == "1":
        return MuseClass("Muse", 30, 40)
    elif choice == "2":
        return SoldierClass("Soldier", 45, 55)
    elif choice == "3":
        return HawkerClass("Hawker", 35, 45)
    elif choice == "4":
        return DealerClass("Dealer", 20, 40)
    else:
        return None


def evolve_character(character):
    new_character = character
    if character.name == "Muse":
        if random.randint(1, 2) == 1:
            new_character = ClericClass("Cleric", 45, 55)
        else:
            new_character = MageClass("Mage", 60, 75)
    elif character.name == "Soldier":
        if random.randint(1, 2) == 1:
            new_character = KnightClass("Knight", 70, 80)
        else:
            new_character = ChampionClass("Champion", 65, 80)
    elif character.name == "Hawker":
        if random.randint(1, 2) == 1:
            new_character = ScoutClass("Scout", 55, 70)
        else:
            new_character = RaiderClass("Raider", 60, 80)

    if new_character != character:
        new_character.health = character.health
        new_character.mana = character.mana
        new_character.skip_rounds = character.skip_rounds
        new_character.fire_rounds = character.fire_rounds
        new_character.bleed_rounds = character.bleed_rounds
        new_character.arrow_poison_rounds = character.arrow_poison_rounds
        new_character.knife_poison_rounds = character.knife_poison_rounds
        new_character.reflect_percent = character.reflect_percent
        new_character.round_number = character.round_number
        print(character.name, "evolves into", new_character.name)

    return new_character


def apply_fire(character):
    if character.fire_rounds > 0 and character.is_alive():
        character.take_damage(5)
        character.fire_rounds = character.fire_rounds - 1
        print(character.name, "takes 5 fire damage")


def apply_bleed(character):
    if character.bleed_rounds > 0 and character.is_alive():
        character.take_damage(5)
        character.bleed_rounds = character.bleed_rounds - 1
        print(character.name, "takes 5 bleeding damage")


def apply_poison(character):
    if character.arrow_poison_rounds > 0 and character.is_alive():
        character.take_damage(5)
        character.arrow_poison_rounds = character.arrow_poison_rounds - 1
        print(character.name, "takes 5 poison damage from arrow")

    if character.knife_poison_rounds > 0 and character.is_alive():
        character.take_damage(8)
        character.knife_poison_rounds = character.knife_poison_rounds - 1
        print(character.name, "takes 8 poison damage from knife")


def apply_camouflage(character):
    if character.name == "Raider":
        character.hidden_attack = False
        if character.camouflage_rounds > 0 and character.is_alive():
            cost = character.mana * 0.05
            character.mana = character.mana - cost
            character.camouflage_rounds = character.camouflage_rounds - 1
            character.hidden_attack = True
            print(character.name, "is hidden and spends", round(cost, 2), "MP")


def mage_spell(mage, enemy):
    spell = random.randint(1, 3)
    if spell == 1:
        mage.use_fireball(enemy)
    elif spell == 2:
        mage.use_ice_ball(enemy)
    else:
        mage.use_lightning_ball(enemy)


def scout_shot(scout, enemy):
    shot = random.randint(1, 3)
    if shot == 1:
        scout.use_tripple_shot(enemy)
    elif shot == 2:
        scout.use_eagle_shot(enemy)
    else:
        scout.use_poison_arrow(enemy)


def advanced_turn(character, enemy):
    if character.name == "Cleric":
        action = random.randint(1, 6)
        success = True
        if action == 1:
            character.attack(enemy)
        elif action == 2:
            success = character.use_greater_heal()
        elif action == 3:
            success = character.use_mana_restore()
        elif action == 4:
            success = character.use_attack_up()
        elif action == 5:
            success = character.use_defense_up()
        else:
            success = character.use_critical_hit_enhance()
        if success == False:
            character.attack(enemy)

    elif character.name == "Mage":
        action = random.randint(1, 5)
        if action == 1:
            character.attack(enemy)
        elif action == 2:
            character.use_fireball(enemy)
        elif action == 3:
            character.use_ice_ball(enemy)
        elif action == 4:
            character.use_lightning_ball(enemy)
        else:
            if character.use_quick_cast():
                mage_spell(character, enemy)
                if enemy.is_alive():
                    mage_spell(character, enemy)
            else:
                character.attack(enemy)

    elif character.name == "Knight":
        action = random.randint(1, 6)
        if action == 1:
            character.attack(enemy)
        elif action == 2:
            if character.use_enhance_defence() == False:
                character.attack(enemy)
        elif action == 3:
            character.use_shield_reflect()
        elif action == 4:
            character.use_impact_wave(enemy)
        elif action == 5:
            character.use_shield_slam(enemy)
        else:
            character.use_one_hand_attack(enemy)

    elif character.name == "Champion":
        action = random.randint(1, 5)
        if action == 1:
            character.attack(enemy)
        elif action == 2:
            if character.use_berserk() == False:
                character.attack(enemy)
        elif action == 3:
            if character.use_blood_attack(enemy) == False:
                character.attack(enemy)
        elif action == 4:
            character.use_piercing_stab(enemy)
        else:
            character.use_leap_strike(enemy)

    elif character.name == "Scout":
        action = random.randint(1, 5)
        if action == 1:
            character.attack(enemy)
        elif action == 2:
            character.use_tripple_shot(enemy)
        elif action == 3:
            character.use_eagle_shot(enemy)
        elif action == 4:
            character.use_poison_arrow(enemy)
        else:
            if character.use_speed_shot():
                scout_shot(character, enemy)
                if enemy.is_alive():
                    scout_shot(character, enemy)
            else:
                character.attack(enemy)

    elif character.name == "Raider":
        if character.hidden_attack == True:
            character.attack(enemy)
        else:
            action = random.randint(1, 6)
            if action == 1:
                character.attack(enemy)
            elif action == 2:
                character.use_double_slash(enemy)
            elif action == 3:
                character.use_camouflage()
            elif action == 4:
                character.use_screw_attack(enemy)
            elif action == 5:
                character.use_posion_knife(enemy)
            else:
                if character.use_mana_blood(enemy) == False:
                    character.attack(enemy)


def player_turn(player, enemy):
    apply_camouflage(player)
    if player.skip_rounds > 0:
        player.skip_rounds = player.skip_rounds - 1
        print(player.name, "skips this turn")
        return

    if player.name == "Cleric" or player.name == "Mage" or player.name == "Knight" or player.name == "Champion" or player.name == "Scout" or player.name == "Raider":
        advanced_turn(player, enemy)
        return

    print("1 - Basic attack")
    if player.name == "Dealer":
        print("2 - Gun")
    elif player.name == "Hawker":
        print("2 - Bow")
        print("3 - Stealth")

    action = input("Choose an action: ")
    if player.name == "Dealer" and action == "2":
        player.use_gun(enemy)
    elif player.name == "Hawker" and action == "2":
        player.use_bow(enemy)
    elif player.name == "Hawker" and action == "3":
        if player.use_stealth() == False:
            player.attack(enemy)
    else:
        player.attack(enemy)


def enemy_turn(enemy, player):
    apply_camouflage(enemy)
    if enemy.skip_rounds > 0:
        enemy.skip_rounds = enemy.skip_rounds - 1
        print(enemy.name, "skips this turn")
        return

    if enemy.name == "Dealer":
        action = random.randint(1, 2)
        if action == 1:
            enemy.attack(player)
        else:
            enemy.use_gun(player)
    elif enemy.name == "Hawker":
        action = random.randint(1, 3)
        if action == 1:
            enemy.attack(player)
        elif action == 2:
            enemy.use_bow(player)
        else:
            if enemy.use_stealth() == False:
                enemy.attack(player)
    elif enemy.name == "Cleric" or enemy.name == "Mage" or enemy.name == "Knight" or enemy.name == "Champion" or enemy.name == "Scout" or enemy.name == "Raider":
        advanced_turn(enemy, player)
    else:
        enemy.attack(player)


def play_game():
    print("Choose your character and opponent:")
    print("1 - Muse")
    print("2 - Soldier")
    print("3 - Hawker")
    print("4 - Dealer")

    player_choice = input("Your character (1-4): ")
    enemy_choice = input("Your opponent (1-4): ")

    player = create_character(player_choice)
    enemy = create_character(enemy_choice)

    if player is None or enemy is None:
        print("Invalid character choice")
    else:
        round_number = 1
        while player.is_alive() and enemy.is_alive():
            player.round_number = round_number
            enemy.round_number = round_number
            print("\nRound", round_number)

            apply_fire(player)
            apply_fire(enemy)
            apply_bleed(player)
            apply_bleed(enemy)
            apply_poison(player)
            apply_poison(enemy)

            if not player.is_alive() and not enemy.is_alive():
                print("Draw")
                break
            elif not player.is_alive():
                print(enemy.name, "wins!")
                break
            elif not enemy.is_alive():
                print(player.name, "wins!")
                break

            player_turn(player, enemy)

            if not player.is_alive():
                print(enemy.name, "wins!")
                break
            elif not enemy.is_alive():
                print(player.name, "wins!")
                break

            enemy_turn(enemy, player)

            print(player.name, "HP:", round(player.health, 2), "MP:", round(player.mana, 2))
            print(enemy.name, "HP:", round(enemy.health, 2), "MP:", round(enemy.mana, 2))

            if not player.is_alive() and not enemy.is_alive():
                print("Draw")
                break
            elif not player.is_alive():
                print(enemy.name, "wins!")
                break
            elif not enemy.is_alive():
                print(player.name, "wins!")
                break

            if round_number == 10:
                player = evolve_character(player)
                enemy = evolve_character(enemy)

            round_number = round_number + 1


play_game()
