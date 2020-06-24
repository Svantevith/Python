import random

import numpy as np
import time
import sys


# Create the class
class Pokemon:
    def __init__(self, name, pokemon_type, moves, stats):
        self.name = name
        self.type = pokemon_type
        self.moves = moves
        self.health = '🟥' * 3 + '🟨' * 5 + '🟨' * 12
        self.attack = stats['ATTACK']
        self.attack_desc = f'<{self.name} GROWLS AGGRESSIVELY...>'
        self.defence = stats['DEFENCE']
        self.cp = int(round((lambda attack, defence: 8 * np.mean([attack, defence]))(self.attack, self.defence)))
        self.skill_damage_ratio = (1, 0.25, 0.5, 0.75)
        self.skill_energy_ratio = (2, 0, 0.5, 1)
        self.skill_special_bar = 0

    def pokemonDesc(self):
        return f'{self.name}\n' \
               f'TYPE/ {self.type}\n' \
               f'ATTACK/ {self.attack}\n' \
               f'DEFENCE/ {self.defence}\n' \
               f'CP/ {self.cp}\n\n'

    def setSkillEnergyRatio(self):
        for energy_needed in self.skill_energy_ratio:
            energy_needed *= self.attack

    def typeVariance(self, enemy):
        self.attack = round(self.attack * 2)
        self.defence = round(self.defence * 2)
        enemy.attack = round(enemy.attack / 2)
        enemy.defence = round(enemy.defence / 2)

    def setPokemonBonusForType(self, enemy):
        pokemon_types = ('Bug', 'Dark', 'Dragon', 'Electric', 'Fairy', 'Fighting', 'Fire', 'Flying', 'Ghost', 'Grass',
                         'Ground', 'Ice', 'Normal', 'Poison', 'Psychic', 'Rock', 'Steel', 'Water')
        strong_against = (
            ('Grass', 'Dark', 'Psychic'), ('Ghost', 'Psychic'), ('Dragon'), ('Flying', 'Water'),
            ('Fighting', 'Dark', 'Dragon'), ('Dark', 'Ice', 'Normal', 'Rock', 'Steel'),
            ('Bug', 'Grass', 'Ice', 'Steel'), ('Bug', 'Fighting', 'Grass'), ('Ghost', 'Psychic'),
            ('Ground', 'Rock', 'Water'), ('Electric', 'Fire', 'Poison', 'Rock', 'Steel'),
            ('Dragon', 'Flying', 'Grass', 'Ground'), (None), ('Fairy', 'Grass'), ('Fighting', 'Poison'),
            ('Bug', 'Fire', 'Flying', 'Ice'), ('Fairy', 'Ice', 'Rock'), ('Fire', 'Ground', 'Rock')
        )
        weak_against = (
            ('Fire', 'Flying', 'Rock'), ('Bug', 'Fire', 'Lightning'), ('Dragon', 'Fairy', 'Ice'), ('Ground'),
            ('Poison', 'Steel'), ('Fairy', 'Flying', 'Psychic'), ('Ground', 'Rock', 'Water'),
            ('Electric', 'Ice', 'Rock'), ('Dark', 'Ghost'), ('Bug', 'Fire', 'Flying', 'Ice', 'Poison'),
            ('Grass', 'Ice', 'Water'), ('Fighting', 'Fire', 'Rock', 'Steel'), ('Fighting'), ('Ground', 'Psychic'),
            ('Bug', 'Dark', 'Ghost'), ('Fighting', 'Grass', 'Ground', 'Steel', 'Water'),
            ('Fighting', 'Fire', 'Ground'), ('Electric', 'Grass')
        )

        attack_info = ("It's not very effective", "It's super effective!")

        # Case 1: Both Pokemons are same type
        if enemy.type == self.type:
            self.attack_desc = attack_info[0]
            enemy.attack_desc = attack_info[0]

        # Case 2: My Pokemon is stronger
        if enemy.type in strong_against[pokemon_types.index(self.type)]:
            self.typeVariance(enemy)  # self *2, enemy / 2
            self.attack_desc = attack_info[1]
            enemy.attack_desc = attack_info[0]

        # Case 3: Enemy Pokemon is stronger
        if enemy.type in weak_against[pokemon_types.index(self.type)]:
            enemy.typeVariance(self)  # enemy *2 , self / 2
            self.attack_desc = attack_info[0]
            enemy.attack_desc = attack_info[1]

    @property
    def skill(self):
        for index, move in enumerate(self.moves):
            print(f'{index + 1}.', move)
        while True:
            user_input = input('Pick a move: ')
            if user_input.isdigit() and int(user_input) in range(1, 4 + 1):
                skill_index = int(user_input)
                print(f'{self.name}, {self.attack}, {self.skill_special_bar},'
                      f' {self.skill_energy_ratio[skill_index - 1] * self.attack}')
                if self.skill_special_bar >= self.skill_energy_ratio[skill_index - 1] * self.attack:
                    self.skill_special_bar -= self.skill_energy_ratio[skill_index - 1] * self.attack
                    print(f'{self.name}, {self.skill_special_bar}')
                    self.skill_special_bar += self.attack
                    print(f'{self.name}, {self.skill_special_bar}')
                    break
                else:
                    delayPrint(f'{self.name} cannot use that attack now\n')
            else:
                print('Your input should be an integer in the range between 1 and 4!')

        delayPrint(f'{self.name} used {self.moves[skill_index - 1]}\n')
        time.sleep(1)
        return skill_index

    def skillDamage(self, enemy):

        skill_index = self.skill

        attack_val = (0, self.attack)
        miss_probability = enemy.cp / (10 * self.cp)  # the higher cp of the attacking pokemon, the less chance for miss
        attack_probability = (miss_probability, 1 - miss_probability)
        attack_list = random.choices(attack_val, attack_probability)
        attack = attack_list[0] * self.skill_damage_ratio[skill_index - 1]
        damage = 0
        try:
            damage = round(attack - 0.1 * (enemy.cp / self.cp) * enemy.defence)
        except ZeroDivisionError:
            damage = 0
        finally:
            if damage <= 0:
                damage = 0
                delayPrint(f"{self.name} missed!\n")
            if damage >= len(enemy.health):
                damage = len(enemy.health)
            return damage

    def pokemonTurn(self, enemy):
        # Print the health of each Pokemon
        print(f'{self.name}\t\tHP\t{self.health}')
        print(f'{enemy.name}\t\tHP\t{enemy.health}')

        # pokemon
        print(f'\nGo {self.name}!')
        # pokemon_types = {Strong Type: against weak Type, ... }
        enemy.health = enemy.health[:len(enemy.health) - self.skillDamage(enemy)]
        delayPrint(self.attack_desc)
        time.sleep(0.5)

        # Print the health of each Pokemon
        print(f'\n{self.name}\t\tHP\t{self.health}')
        print(f'\n{enemy.name}\t\tHP\t{enemy.health}\n')

        return self.health

    def pokemonFight(self, enemy):
        # Print the information
        delayPrint('\n\tPOKEMON BATTLE\n\n')
        delayPrint(self.pokemonDesc())
        delayPrint(enemy.pokemonDesc())

        self.setPokemonBonusForType(enemy)
        self.setSkillEnergyRatio()

        time.sleep(2)

        while len(self.health) > 0 and len(enemy.health) > 0:
            if len(self.pokemonTurn(enemy)) <= 0:  # self attacks enemy
                delayPrint(f"\n...{enemy.name} fainted.")
                break
            if len(enemy.pokemonTurn(self)) <= 0:  # enemy attack self
                delayPrint(f"\n...{self.name} fainted.")
                break

        money = np.random.choice(5000)
        delayPrint(f"You've obtained {money} Stardust!")


# delay printing
def delayPrint(string):
    # print one character in a specific time interval
    for char in string:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(5e-2)


if __name__ == '__main__':
    # Create Pokemon
    charizard = Pokemon('Charizard', 'Fire', ['Flamethrower', 'Fly', 'Blast Burn', 'Fire Punch'],
                        {'ATTACK': 18, 'DEFENCE': 10})
    blastoise = Pokemon('Blastoise', 'Water', ['Water Gun', 'Bubblebeam', 'Hydro Pump', 'Surf'],
                        {'ATTACK': 8, 'DEFENCE': 12})
    venusaur = Pokemon('Venusaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Earthquake', 'Frenzy Plant'],
                       {'ATTACK': 8, 'DEFENCE': 12})

    charmander = Pokemon('Charmander', 'Fire', ['Ember', 'Scratch', 'Tackle', 'Fire Punch'],
                         {'ATTACK': 4, 'DEFENCE': 2})
    squirtle = Pokemon('Squirtle', 'Water', ['Bubblebeam', 'Tackle', 'Headbutt', 'Surf'], {'ATTACK': 3, 'DEFENCE': 3})
    bulbasaur = Pokemon('Bulbasaur', 'Grass', ['Vine Wip', 'Razor Leaf', 'Tackle', 'Leech Seed'],
                        {'ATTACK': 2, 'DEFENCE': 4})

    charmeleon = Pokemon('Charmeleon', 'Fire', ['Ember', 'Scratch', 'Flamethrower', 'Fire Punch'],
                         {'ATTACK': 6, 'DEFENCE': 5})
    wartortle = Pokemon('Wartortle', 'Water', ['Bubblebeam', 'Water Gun', 'Headbutt', 'Surf'],
                        {'ATTACK': 5, 'DEFENCE': 5})
    ivysaur = Pokemon('Ivysaur\t', 'Grass', ['Vine Wip', 'Razor Leaf', 'Bullet Seed', 'Leech Seed'],
                      {'ATTACK': 4, 'DEFENCE': 6})

    charizard.pokemonFight(blastoise)
