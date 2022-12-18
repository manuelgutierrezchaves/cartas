import random
import utils
import os
from collections import Counter
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


class Card:
    def __init__(self, name, cost, attack):
        self.name = name
        self.cost = cost
        self.attack = attack


class Player:
    def __init__(self, cards_path):
        card_list = utils.json2list(cards_path)
        self.deck = [Card(name=card_values['name'],
                          cost=card_values['cost'],
                          attack=card_values['attack'],
                          ) for card_values in card_list]
        self.suffle_deck()
        self.hand = []
        self.deal_hand(3)  # Reparte 3 al inicio

    def suffle_deck(self):
        random.shuffle(self.deck)

    def deal_hand(self, quantity):
        choosen_cards = random.sample(self.deck, quantity)
        for card in choosen_cards:
            self.deck.remove(card)
        self.hand.extend(choosen_cards)

    def remove_card_from_hand(self, card):
        self.hand.remove(card)




class Location:
    def __init__(self):
        self.cards = {'top': [], 'bottom': []}
        self.update()

    def add_card(self, player, card):  # player == 'top' or 'bottom'
        self.cards[player].append(card)
        self.update()

    def update(self):
        self.top_points = sum(card.attack for card in self.cards['top'])
        self.bottom_points = sum(card.attack for card in self.cards['bottom'])

    def check_location_winner(self):
        self.update()
        if self.top_points == self.bottom_points:
            return 'empate'
        elif self.top_points > self.bottom_points:
            return 'top'
        elif self.top_points < self.bottom_points:
            return 'bottom'


class Game:
    def __init__(self):
        self.turn = 1
        self.locations = {'left': Location(),
                          'center': Location(),
                          'right': Location()}
        self.bottom_player = Player('/src/cartas_1.json')
        self.top_player = Player('/src/cartas_2.json')

    def __repr__(self) -> str:
        nombres = ""
        costes = ""
        ataques = ""

        for carta in self.bottom_player.hand:
            nombres += carta.name + 4*" "
            costes += str(carta.cost).center(len(carta.name), " ") + 4*" "
            ataques += str(carta.attack).center(len(carta.name), " ") + 4*" "

        return f'\n\n{nombres}\n{costes}\n{ataques}\n\nTurn: {self.turn}'

    def show_locations(self):
        location_names = ''
        for location_name in self.locations.keys():
            location_names += location_name + 4*" "
        print(location_names)

    def play_card(self, player, location, card):
        if player == 'bottom':
            self.bottom_player.remove_card_from_hand(card)
            self.locations[location].add_card(player, card)

    def check_game_winner(self):
        winner_locations = [location.check_location_winner() for location in self.locations.values()]
        contador = Counter(winner_locations)
        elementos_ordenados = contador.most_common()  # [('top', 2), ('bottom', 1)]
        return elementos_ordenados[0][0]


def play_game():
    game = Game()
    location_numbers = {1: 'left', 2: 'center', 3: 'right'}

    while game.turn <= 6:
        # game.show_locations()
        # print(game)
        game.bottom_player.deal_hand(1)
        game.top_player.deal_hand(1)

        # Mostrar pantalla
        game.show_locations()
        print(game)

        # Pedir al jugador que elija una ubicación
        location_num = int(input("\n\n1 - left\n2 - center\n3 - right\n\nElige una ubicación: "))
        location = location_numbers[location_num]

        clear()
        # Mostrar pantalla
        game.show_locations()
        print(game)
        print('\n')

        # Pedir al jugador que elija una carta
        for idx, card in enumerate(game.bottom_player.hand):
            print(f'{idx+1} - {card.name}')
        card_index = int(input('\nEscoge una carta: '))
        clear()
        card = game.bottom_player.hand[card_index-1]

        # Comprobar energia
        if card.cost > game.turn:
            print("No tienes suficientes puntos para jugar esa carta.")
        else:
            # Jugar la carta
            game.play_card('bottom', location, card)
        game.turn += 1


    # Determinar ganador
    winner = game.check_game_winner()
    clear()
    print(f"El ganador es el jugador {winner}.")


if __name__ == '__main__':
    clear()
    play_game()
    # jugador_1 = Player('cartas_1.json')
    # print(jugador_1.deck[0].name)
    # carta1 = Card('Punisher', 2, 4)
    # carta2 = Card('Medusa', 2, 2)
    # mapa = Location()
    # mapa.add_card('top', carta1)
    # mapa.add_card('top', carta2)
    # mapa.check_winner()