import random

ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8,
          'Nine': 9, 'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': [1, 11]}

playing = True

class Card:

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit


class Deck:

    def __init__(self):
        self.all_cards = []

        for rank in ranks:
            for suit in suits:
                self.all_cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.all_cards)

    def deal_one(self):
        return self.all_cards.pop()


class Bank:

    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance

    def __str__(self):
        return "Balance: $%s" % self.balance

    def win_deposit(self, amount):
        self.balance += amount * 2
        print('You now have $%s' % self.balance)

    def money_back(self, amount):
        self.balance += amount
        print('You now have $%s' % self.balance)

    def bet_value(self):
        bet = ''
        while not (bet.isdigit()) or int(bet) > player_bank.balance:
            bet = input(
                'Bet needs to be a # and fit your balance of $%s. Place your bet: ' % player_bank.balance)
        return bet

    def place_bet(self, amount):
        self.amount = amount

        self.balance -= self.amount
        print('Bet is placed! Your balance is now $%s ' % self.balance)


class Player_or_Dealer:  # aka CHOICES

    def __init__(self, name):
        self.name = name
        self.all_cards = []

    def hit(self, new_card):
        self.all_cards.append(new_card)

    def sum_of_values(self):
        total = 0
        num_aces = 0

        for num in range(len(self.all_cards)):     # go though all the cards
            if self.all_cards[num].rank != 'Ace':  # add all cards that arent Aces
                total += self.all_cards[num].value
            if self.all_cards[num].rank == 'Ace':  # if Ace, count the number of Aces
                num_aces += 1

        # depending on # of Acves decide of on their points
        # (num_aces - 1) = 1 point for every Ace + 11 points for one Ace
        if num_aces == 1 and total + 11 <= 21:
            total += values["Ace"][1]
        if num_aces > 1 and total + (num_aces - 1) + 11 <= 21:
            total += (num_aces - 1) + values["Ace"][1]
        else:
            total += num_aces

        return total

while True:

    new_deck = Deck()
    new_deck.shuffle()

    player = Player_or_Dealer('Player')
    dealer = Player_or_Dealer('Dealer')

    player_bank = Bank(player, 100)

    # player places bet
    bet = player_bank.bet_value()
    player_bank.place_bet(int(bet))

    while playing:
        # 2 cards to player  - game on
        for num in range(2):
            player.hit(new_deck.deal_one())
            print(f'Player: {player.all_cards[-1]}')

        # 1 card to dealer
        # one face down
        for num in range(2):
            dealer.hit(new_deck.deal_one())
        print(f'Dealer: {dealer.all_cards[-1]} + 1 card face down')

     # Player HIT or STAY:
        hit = ''
        while not hit == 's':
            hit = input("Press 'h' for HIT or 's' for STAY: ").lower()

            if hit == 'h':
                player.hit(new_deck.deal_one())
                print(f'Player + {player.all_cards[-1]}')
            if hit == 's':
                playing = False

    # show both Dealer's cards
    print(f'Dealer + {dealer.all_cards[0]}')
    while dealer.sum_of_values() < 17:
        dealer.hit(new_deck.deal_one())
        print(f'Dealer +  {dealer.all_cards[-1]}')
        break

    print(f'Player: {player.sum_of_values()}')
    print(f"Dealer: {dealer.sum_of_values()}")

    if dealer.sum_of_values() > 21:
        print(f'Player wins and doubles his bet! + ${int(bet) * 2}')
        player_bank.win_deposit(int(bet))
        player_bank.__str__()


    elif player.sum_of_values() < 22 and (21 - player.sum_of_values()) < (21 - dealer.sum_of_values()):
        print(f'Player wins and doubles his bet! + ${int(bet) * 2}')
        player_bank.win_deposit(int(bet))
        player_bank.__str__()

    elif player.sum_of_values() == dealer.sum_of_values() and player.sum_of_values() < 22:
        print('This is a tie. Player gets his money back.')
        player_bank.money_back(int(bet))

    else:
        print('Player lost. Your balance is now $%s ' % player_bank.balance)


    new_game = input("Would you like to play another game? Enter 'y' or 'n' ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thanks for playing!")
        break
