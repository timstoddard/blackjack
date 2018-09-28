class Card:
  def __init__(self, deckId, suit, number):
    self.deckId = deckId
    self.suit = suit
    self.number = number

  def toString(self):
    return f'[ {self.number} ]'

  def toStringDetailed(self):
    return f'{self.number} of {self.suit}'
