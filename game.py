import tkinter as tk
from PIL import Image, ImageTk
import random
from pathlib import Path
from classes import Player


class Game:
    def __init__(self) -> None:
        self.img_dir = Path(__file__).parent / 'pictures'
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window['pady'] = 30
        self.window['padx'] = 30

        self.window.bind('<Escape>', lambda _: self.window.destroy())
        self.font_size = min(
            self.window.winfo_screenwidth(),
            self.window.winfo_screenheight()
        ) // 50
        self.window.option_add('*Font', ('Impact', self.font_size))

        self.image_size = self.window.winfo_screenwidth() // 3

        self.player = Player('Вася Питонов', 'vasya.png', 1, 10, 0)
        self.enemy = None

        self.player_frame = tk.Frame(self.window)
        self.player_frame.pack(side='left')

        self.enemy_frame = tk.Frame(self.window)
        self.enemy_frame.pack(side='right')

        self.combat_frame = tk.Frame(self.window)
        self.combat_frame.pack(side='left', expand=True, fill='both')

        self.combat_messages = tk.Listbox(self.combat_frame)
        self.combat_messages.pack(expand=True, fill='both')

        self.attack_button = tk.Button(
            self.combat_frame, borderwidth=5, text='атака', command=self.attack
        )
        self.attack_button.pack(pady=50, ipadx=50, ipady=50)

        self.restart_fight_button = tk.Button(
            self.combat_frame, borderwidth=5, text='Следующий враг', command=self.start_new_fight
        )
        self.restart_fight_button.pack()

        self.heroes_image_tk = dict()
        self.remake_hero_widgets(self.player, self.player_frame)
        self.restart_fight_button['state'] = 'normal'
        self.attack_button['state'] = 'disabled'
        self.window.mainloop()

    def remake_hero_widgets(self, hero: Player, frame: tk.Frame) -> None:
        '''Удаляет и создает виджеты героя'''
        for widget in frame.winfo_children():
            widget.destroy()
        image = Image.open(self.img_dir / hero.image)
        image = image.resize((self.image_size, self.image_size))
        self.heroes_image_tk[hero.name] = ImageTk.PhotoImage(image=image)

        tk.Label(frame, image=self.heroes_image_tk[hero.name]).pack()

        tk.Label(frame, text=hero.name).pack()
        self.player_hp = tk.Label(frame, text=f'жизни: {hero.hp}')
        self.player_hp.pack()

        tk.Label(frame, text=f'уровень: {hero.lvl}').pack()
        tk.Label(frame, text=f'опыт: {hero.exp}').pack()
        tk.Label(frame, text=f'атака: {hero.attack_power}').pack()
        tk.Label(frame, text=f'оружие: {hero.weapon}').pack()

    def start_new_fight(self) -> None:
        '''Начинает новое сражение'''
        self.enemy = Player('Зомби', 'Zombie.png', 1, 10, 0)
        self.attack_button['state'] = 'normal'
        self.restart_fight_button['state'] = 'disabled'
        self.remake_hero_widgets(self.enemy, self.enemy_frame)
        #TODO: создать нового противника
        self.combat_messages.delete(0, tk.END)
        pass

    def combat_turn(self, attacker: Player, defender: Player) -> None:
        if attacker.hp <= 0:
            self.call_winner(defender)
            return
        elif defender.hp <= 0:
            self.call_winner(attacker)
            return
        defender.hp = max(defender.hp - attacker.attack_power, 0)
        text = f'{attacker.name} атаковал {defender.name} на {attacker.attack_power} hp'
        self.combat_messages.insert(tk.END, text)

    def call_winner(self, winner: Player) -> None:
        text = f'{winner.name} Победил'
        self.combat_messages.insert(tk.END, text)
        self.attack_button['state'] = 'disabled'
        self.restart_fight_button['state'] = 'normal'

    def attack(self) -> None:
        self.combat_turn(self.player, self.enemy)
        self.combat_turn(self.enemy, self.player)
        # TODO: раздать награды
        self.remake_hero_widgets(self.player, self.player_frame)
        self.remake_hero_widgets(self.enemy, self.enemy_frame)


Game()





'''
if player_xp % 10 == 0:
    player_level += player_xp // 10
    player_xp += enemy_level % 10
'''