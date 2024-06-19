from os import system


class Player:
    def __init__(self, name: str, image: str, lvl: int, hp: int, exp: int, weapon=None) -> None:
        self.name = name
        self.hp = hp  # экземплярный атрибут
        self.image = image
        self.lvl = lvl
        self.exp = exp
        self.weapon_default = Weapon(1, 'Кулаки')
        if weapon:
            self.weapon = weapon
        else:
            self.weapon = self.weapon_default
        self.attack_power = self.weapon.weapon_power * self.lvl
        self.inventory = []

    def attack(self, enemy) -> None:
        '''Обмен ударами'''
        system('cls')
        # атака соперника
        if self.hp <= 0:
            return
        damage = self.attack_power + self.weapon.attack_power
        enemy.hp -= damage
        print(
            self.name,
            'атаковал',
            enemy.name,
            'на',
            damage
        )


class Weapon:
    '''Оружие'''
    def __init__(self, attack_power: int, name: str) -> None:
        self.name = name
        self.weapon_power = attack_power  # влияет на атаку игрока

    def __str__(self) -> str:
        return f'{self.name} ({self.weapon_power})'
