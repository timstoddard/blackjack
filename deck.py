from random import shuffle
from constants import ALL_NUMBERS, ALL_SUITS
from card import Card

class Deck:
  def __init__(self, numberOfDecks):
    self.numberOfDecks = numberOfDecks
    self.initDeck()

  # initializes a list of cards to serve as the deck and shuffles them
  def initDeck(self):
    availableCards = []
    for i in range(0, self.numberOfDecks):
      for suit in ALL_SUITS:
        for number in ALL_NUMBERS:
          availableCards.append(Card(i, suit, number))
    self.availableCards = availableCards
    self.discardedCards = []
    shuffle(self.availableCards)

  # draws a single card from the deck
  def draw(self):
    if (len(self.availableCards) == 0):
      if (len(self.discardedCards) > 0):
        shuffle(self.discardedCards)
        self.availableCards = self.discardedCards
        self.discardedCards = []
        return self.availableCards.pop()
      else:
        print('Uh oh, there are no cards left in the deck! Try using more decks next time.')
        exit(-1)
    return self.availableCards.pop()

  # discards the given card
  def discard(self, card):
    self.discardedCards.append(card)

  def toString(self):
    print('AVAILABLE', [card.toString() for card in self.availableCards])
    print('DISCARDED', [card.toString() for card in self.discardedCards])
