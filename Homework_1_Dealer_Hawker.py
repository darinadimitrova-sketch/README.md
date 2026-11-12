import random


class CharacterClass:
    def __init__(self, name, min_damage, max_damage):
        self.name = name
        self.health = 1000
        self.mana = 500
        self.min_damage = min_damage
        self.max_damage = max_damage
        self.skip_rounds = 0

    def attack(self, enemy):
        damage = random.randint(self.min_damage, self.max_damage)
        enemy.health = enemy.health - damage
        if enemy.health < 0:
            enemy.health = 0
        print(self.name, "attacks for", damage, "damage")

    def heal(self, amount):
        self.health = self.health + amount
        if self.health > 1000:
            self.health = 1000

    def is_alive(self):
        return self.health > 0


class DealerClass(CharacterClass):
    def use_gun(self, enemy):
        damage = enemy.health * 0.55
        enemy.health = enemy.health - damage
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
        else:
            print(self.name, "does not have enough mana")

    def use_bow(self, enemy):
        damage = enemy.health * 0.35
        enemy.health = enemy.health - damage
        print(self.name, "uses bow for", round(damage, 2), "damage")

        chance = random.randint(1, 3)
        if chance == 1 and enemy.is_alive():
            enemy.skip_rounds = enemy.skip_rounds + 1
            print(enemy.name, "must skip 1 turn")


def create_character(choice):
    if choice == "1":
        return DealerClass("Dealer", 20, 40)
    elif choice == "2":
        return HawkerClass("Hawker", 35, 45)
    else:
        return None


print("1 - Dealer")
print("2 - Hawker")

player_choice = input("Choose your character: ")
enemy_choice = input("Choose your opponent: ")

player = create_character(player_choice)
enemy = create_character(enemy_choice)

if player is None or enemy is None:
    print("Invalid character choice")
else:
    round_number = 1

    while player.is_alive() and enemy.is_alive():
        print("\nRound", round_number)

        if player.skip_rounds > 0:
            player.skip_rounds = player.skip_rounds - 1
            print("Your character skips this turn")
        else:
            print("1 - Basic attack")
            if player.name == "Dealer":
                print("2 - Gun")
            else:
                print("2 - Bow")
                print("3 - Stealth")

            action = input("Choose an action: ")

            if action == "2":
                if player.name == "Dealer":
                    player.use_gun(enemy)
                else:
                    player.use_bow(enemy)
            elif action == "3" and player.name == "Hawker":
                if player.mana >= 20:
                    player.use_stealth()
                else:
                    print("Not enough mana. Using a basic attack")
                    player.attack(enemy)
            else:
                player.attack(enemy)

        if not enemy.is_alive():
            print("You win!")
            break

        if enemy.skip_rounds > 0:
            enemy.skip_rounds = enemy.skip_rounds - 1
            print("Opponent skips this turn")
        else:
            if enemy.name == "Dealer":
                action = random.randint(1, 2)
                if action == 1:
                    enemy.attack(player)
                else:
                    enemy.use_gun(player)
            else:
                action = random.randint(1, 3)
                if action == 1:
                    enemy.attack(player)
                elif action == 2:
                    enemy.use_bow(player)
                else:
                    if enemy.mana >= 20:
                        enemy.use_stealth()
                    else:
                        enemy.attack(player)

        print("Your", player.name, "- HP:", round(player.health, 2), "MP:", player.mana)
        print("Opponent", enemy.name, "- HP:", round(enemy.health, 2), "MP:", enemy.mana)

        if not player.is_alive():
            print("Opponent wins!")
            break

        round_number = round_number + 1
