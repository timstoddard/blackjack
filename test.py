import unittest
from card import Card
from player import Player
from game import formatWinningPlayerNames, getPlayerWithBestTotal

class TestPlayer(unittest.TestCase):
  # Player.getTotals() tests
  def test_getTotal_noAces(self):
    p = Player('')
    p.addCard(Card(0, 'spades', '2'))
    self.assertEqual(p.getTotals(), [2])
    p.addCard(Card(0, 'spades', '4'))
    self.assertEqual(p.getTotals(), [6])
    p.addCard(Card(0, 'spades', '7'))
    self.assertEqual(p.getTotals(), [13])

  def test_getTotal_singleAce(self):
    p = Player('')
    p.addCard(Card(0, 'spades', 'A'))
    self.assertEqual(p.getTotals(), [1, 11])
    p.addCard(Card(0, 'spades', '4'))
    self.assertEqual(p.getTotals(), [5, 15])
    p.addCard(Card(0, 'spades', '3'))
    self.assertEqual(p.getTotals(), [8, 18])

  def test_getTotal_multipleAces(self):
    p = Player('')
    p.addCard(Card(0, 'spades', 'A'))
    self.assertEqual(p.getTotals(), [1, 11])
    p.addCard(Card(0, 'spades', 'A'))
    self.assertEqual(p.getTotals(), [2, 12])

  # getPlayerWithBestTotal() tests
  def test_getPlayerWithBestTotal_singleWinner(self):
    a = Player('')
    a.setFinalTotal(1)
    b = Player('')
    b.setFinalTotal(0)
    players = [a, b]
    result = getPlayerWithBestTotal(players)
    self.assertEqual(result, [a])

  def test_getPlayerWithBestTotal_tie(self):
    a = Player('')
    a.setFinalTotal(1)
    b = Player('')
    b.setFinalTotal(1)
    players = [a, b]
    result = getPlayerWithBestTotal(players)
    self.assertEqual(result, [a, b])

  # formatWinningPlayerNames() tests
  def test_formatWinningPlayerNames_singleWinner(self):
    a = Player('a')
    players = [a]
    result = formatWinningPlayerNames(players)
    self.assertEqual(result, 'a')

  def test_formatWinningPlayerNames_twoWinners(self):
    a = Player('a')
    b = Player('b')
    players = [a, b]
    result = formatWinningPlayerNames(players)
    self.assertEqual(result, 'a and b')

  def test_formatWinningPlayerNames_moreThanTwoWinners(self):
    a = Player('a')
    b = Player('b')
    c = Player('c')
    players = [a, b, c]
    result = formatWinningPlayerNames(players)
    self.assertEqual(result, 'a, b, and c')

if __name__ == '__main__':
    unittest.main()
