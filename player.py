from itertools import product
from functools import reduce
from constants import VALUE_MAP

class Player:
  def __init__(self, name):
    self.name = name
    self.totals = []
    self.finalTotal = 0

  # add a card to the player's hand
  def addCard(self, card):
    self.hand.append(card)
    self.totals = self.generateTotals()

  # generates a new hand for the player
  def generateHand(self, deck):
    self.hand = []
    self.addCard(deck.draw())
    self.addCard(deck.draw())

  # discards the player's hand
  def discardHand(self, deck):
    for card in self.hand:
      deck.discard(card)
    self.hand = []

  # generates all possible totals
  # (Ace can be 1 or 11 so multiple totals can happen)
  def generateTotals(self, doFilter=True):
    # get numerical values for each card
    values = [VALUE_MAP[card.number] for card in self.hand]

    # find all possible totals
    currentValue = values.pop()
    while (len(values) > 0):
      nextCurrentValue  = []
      # take the cartesian product of the 2 lists
      for n in product(currentValue, values.pop()):
        # append the sum of each resulting list
        nextCurrentValue.append(reduce((lambda x, y: x + y), n))
      currentValue = nextCurrentValue

    # filter any totals >21
    if (doFilter):
      currentValue = [n for n in currentValue if n <= 21]

    # remove duplicates and sort the list
    currentValue = list(set(currentValue))
    currentValue.sort()
    return currentValue

  def getTotals(self):
    return self.totals

  # prints all totals currently possible for the player
  def printTotals(self):
    return self.formatTotals(self.totals)

  # formats the totals for printing
  def formatTotals(self, totals):
    totalsString = ' or '.join([str(total) for total in totals])
    modifier = 's' if len(totals) > 1 else ''
    return f'Total{modifier}: {totalsString}'

  def getFinalTotal(self):
    return self.finalTotal

  def setFinalTotal(self, finalTotal):
    self.finalTotal = finalTotal

  # prints all the cards in the player's hand, plus all their possible totals
  def printHand(self, showOnlyMax=False, showOnlyMin=False, detailed=False):
    result = ''
    if (detailed):
      result = '\n'.join([card.toStringDetailed() for card in self.hand])
    else:
      result = ' '.join([card.toString() for card in self.hand])
    totals = self.totals
    if (len(self.totals) == 0):
      totals = self.generateTotals(False)
    if (showOnlyMax):
      totals = [max(totals)]
    elif (showOnlyMin):
      totals = [min(totals)]
    return f'{result}\n{self.formatTotals(totals)}'
