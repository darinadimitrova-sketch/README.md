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
        self.round_number = 1

    def take_damage(self, damage):
        self.health = self.health - damage
        if self.health < 0:
            self.health = 0

    def attack(self, enemy):
        damage = random.randint(self.min_damage, self.max_damage)
        enemy.take_damage(damage)
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
        enemy.take_damage(damage)
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
        enemy.take_damage(damage)
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

        enemy.take_damage(damage)
        print(self.name, "attacks for", round(damage, 2), "damage")

    def take_damage(self, damage):
        if self.round_number < self.defense_end:
            damage = damage * 0.72

        self.health = self.health - damage
        if self.health < 0:
            self.health = 0


class MageClass(MuseClass):
    def __init__(self, name, min_damage, max_damage):
        MuseClass.__init__(self, name, min_damage, max_damage)
        self.quick_cast_ready = 1

    def use_fireball(self, enemy):
        damage = random.randint(50, 80)
        enemy.take_damage(damage)
        print(self.name, "uses Fireball for", damage, "damage")

        if enemy.is_alive():
            enemy.fire_rounds = 3
            print(enemy.name, "will take fire damage for 3 rounds")

    def use_ice_ball(self, enemy):
        damage = random.randint(30, 50)
        enemy.take_damage(damage)
        print(self.name, "uses Ice Ball for", damage, "damage")

        chance = random.randint(1, 100)
        if chance <= 15 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")

    def use_lightning_ball(self, enemy):
        damage = random.randint(60, 70)
        enemy.take_damage(damage)
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
    if character.name == "Muse":
        chance = random.randint(1, 2)
        if chance == 1:
            new_character = ClericClass("Cleric", 45, 55)
        else:
            new_character = MageClass("Mage", 60, 75)

        new_character.health = character.health
        new_character.mana = character.mana
        new_character.skip_rounds = character.skip_rounds
        new_character.fire_rounds = character.fire_rounds
        new_character.round_number = character.round_number
        print(character.name, "evolves into", new_character.name)
        return new_character

    return character


def apply_fire(character):
    if character.fire_rounds > 0 and character.is_alive():
        old_health = character.health
        character.take_damage(5)
        damage = old_health - character.health
        character.fire_rounds = character.fire_rounds - 1
        print(character.name, "takes", round(damage, 2), "fire damage")


def mage_spell(mage, enemy, spell):
    if spell == "1":
        mage.use_fireball(enemy)
    elif spell == "2":
        mage.use_ice_ball(enemy)
    elif spell == "3":
        mage.use_lightning_ball(enemy)
    else:
        mage.use_fireball(enemy)


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
                for number in range(1, 3):
                    if enemy.is_alive():
                        spell = random.randint(1, 3)
                        mage_spell(character, enemy, str(spell))
            else:
                character.attack(enemy)


def player_turn(player, enemy):
    if player.skip_rounds > 0:
        player.skip_rounds = player.skip_rounds - 1
        print(player.name, "skips this turn")
        return

    if player.name == "Cleric" or player.name == "Mage":
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
    elif enemy.name == "Cleric" or enemy.name == "Mage":
        advanced_turn(enemy, player)
    else:
        enemy.attack(player)


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

        if not enemy.is_alive():
            print(player.name, "wins!")
            break

        enemy_turn(enemy, player)

        print(player.name, "HP:", round(player.health, 2), "MP:", round(player.mana, 2))
        print(enemy.name, "HP:", round(enemy.health, 2), "MP:", round(enemy.mana, 2))

        if not player.is_alive():
            print(enemy.name, "wins!")
            break

        if round_number == 10:
            player = evolve_character(player)
            enemy = evolve_character(enemy)

        round_number = round_number + 1
