import random
import utils


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
        self.deal_hand(3)  # Reparte 3 al inicio

    def suffle_deck(self):
        random.shuffle(self.deck)

    def deal_hand(self, quantity):
        self.hand = random.sample(self.deck, quantity)
        for card in self.hand:
            self.deck.remove(card)


class Location:
    def __init__(self):
        self.cards = {'top': [], 'bottom': []}

    def add_card(self, player, card):  # player == 'top' or 'bottom'
        self.cards[player].append(card)

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
        self.bottom_player = Player('cartas_1.json')
        self.top_player = Player('cartas_2.json')


def play_game(num_players):
    game = Game()

    while game.turn <= 6:
        # Repartir una carta a cada jugador al inicio de cada turno
        game.bottom_player.deal_hand(1)
        game.top_player.deal_hand(1)

        # Pedir al jugador que elija una ubicación y una carta para jugar
        player = 0  # Suponemos que sólo hay un jugador en este ejemplo
        print(f"Turno {game.turn}. Tienes {game.points[game.turn - 1]} puntos disponibles.")
        location = int(input("Elige una ubicación (0-2): "))
        card_index = int(input("Elige una carta (0-{}): ".format(len(game.cards[player]) - 1)))
        card = game.cards[player][card_index]
        if card.cost > game.points[game.turn - 1]:
            print("No tienes suficientes puntos para jugar esa carta.")
            continue
        # Jugar la carta
        game.play_card(player, location, card)
        game.points[game.turn - 1] -= card.cost
        game.turn += 1

    # Determinar ganador
    attacks = [sum(card.attack for card in location) for location in game.board]
    winner = attacks.index(max(attacks))
    print(f"El ganador es el jugador {winner} con {attacks[winner]} puntos de ataque.")


if __name__ == '__main__':
    # play_game(2)s
    # jugador_1 = Player('cartas_1.json')
    # print(jugador_1.deck[0].name)
    carta1 = Card('Punisher', 2, 4)
    carta2 = Card('Medusa', 2, 2)
    mapa = Location()
    mapa.add_card('top', carta1)
    mapa.add_card('top', carta2)
    mapa.check_winner()