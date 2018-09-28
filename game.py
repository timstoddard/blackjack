from deck import Deck
from player import Player

# returns a user-inputted positive integer
def getNumericalUserInput(message):
  n = ''
  while (not isinstance(n, int) or n < 1):
    n = input(f'{message} ')
    try:
      n = int(n)
      if (n < 1):
        print('Please enter a positive integer.')
    except ValueError:
      print(f'{n} is not a positive integer; please enter a positive integer.')
  return n

# returns a user-inputted value that is one of the options
def getUserSelectionFromOptions(message, options):
  selection = input(f'{message} ')
  while (not selection in options):
    print(f'{selection} isn\'t an option.')
    print(f'Please choose one of the following options: {", ".join(options)}')
    selection = input(f'{message} ')
  return selection

# returns the player(s) with the best total score
def getPlayerWithBestTotal(players):
  playersWithBestTotal = [players[0]]
  for i in range(1, len(players)):
    player = players[i]
    if (player.getFinalTotal() > playersWithBestTotal[0].getFinalTotal()):
      playersWithBestTotal = [player]
    elif (player.getFinalTotal() == playersWithBestTotal[0].getFinalTotal()):
      playersWithBestTotal.append(player)
  return playersWithBestTotal

# helper method to format a list of names
def formatWinningPlayerNames(winningPlayers):
  names = [player.name for player in winningPlayers]
  if (len(names) == 1):
    return names[0]
  elif (len(names) == 2):
    return f'{names[0]} and {names[1]}'
  else:
    allPlayersExceptLast = winningPlayers[0:len(winningPlayers) - 1]
    temp = ', '.join([player.name for player in allPlayersExceptLast])
    return f'{temp}, and {winningPlayers[len(winningPlayers) - 1].name}'

# guides the users through the setup process where they all input their names and
# returns the list of players
def initPlayers(numberOfPlayers):
  players = []
  for i in range(numberOfPlayers):
    name = input('Player ' + str(i + 1) + ', please tell me your first name: ')
    player = Player(name)
    players.append(player)
    print(f'Welcome, {name}!\n')
  return players

# generate a new hand for every player, including the dealer
def generateAllHands(players, dealer, deck):
  for player in players:
    player.generateHand(deck)
  dealer.generateHand(deck)

def discardAllHands(players, dealer, deck):
  for player in players:
    player.discardHand(deck)
  dealer.discardHand(deck)

# runs the logic for a player to take their turn
def doPlayerTurn(player, deck):
  print(f'Please give the device to {player.name}.\n')
  input(f'{player.name}, press enter to continue.')
  print(f'{player.name}, here is your hand:')
  print(f'{player.printHand()}\n')

  response = ''
  didPlayerBust = False

  # continue the turn while they have not opted to "stay" and have not busted
  while (not response == 's' and didPlayerBust == False):
    response = getUserSelectionFromOptions(
      'Would you like to [h]it, [s]tay, or see [d]etailed info about your hand?',
      ['h', 's', 'd'])
    if (response == 'h'):
      # add a card to their hand
      player.addCard(deck.draw())

      if (len(player.getTotals()) == 0):
        # the player busted
        print('Oh no! You busted. Here is your final hand:')
        print(f'{player.printHand(showOnlyMin=True)}\n')
        didPlayerBust = True
        player.setFinalTotal(False)
      else:
        # the player did not bust, so continues their turn
        print(f'{player.printHand()}\n')
    elif (response == 's'):
      # the player opted to stay
      finalTotal = max(player.getTotals())
      print(f'Okay. Your total is {finalTotal}.\n')
      player.setFinalTotal(finalTotal)
    elif (response == 'd'):
      # print detailed info about the player's hand
      print(f'{player.printHand(detailed=True)}\n')

# runs the logic for the dealer to take their turn
def doDealerTurn(dealer, deck, players):
  input('Now it\'s my turn! Press enter to see how I do.')
  print(f'Here is my hand:')
  print(f'{dealer.printHand()}\n')

  # figure out which player(s) had the best score
  playersWithBestTotal = getPlayerWithBestTotal(players)
  maxPlayerFinalTotal = playersWithBestTotal[0].getFinalTotal()
  winningPlayerNames = formatWinningPlayerNames(playersWithBestTotal)

  isDealersTurn = True
  playAgain = ''

  # continue the dealer's turn while they have neither won nor busted
  while (isDealersTurn):
    if (max(dealer.getTotals()) > maxPlayerFinalTotal):
      # the dealer won
      print('I won! Here is my final hand:')
      print(f'{dealer.printHand(showOnlyMax=True)}\n')
      playAgain = getUserSelectionFromOptions(
        'You guys made that too easy. Want to play again [y/n]?',
        ['y', 'n'])
      isDealersTurn = False
    elif (max(dealer.getTotals()) < maxPlayerFinalTotal):
      # the dealer has not won yet
      print('I choose to hit, let\'s see what I get!')
      dealer.addCard(deck.draw())
      if (len(dealer.getTotals()) == 0):
        # the dealer busted
        print('Oh no! I busted. Here is my final hand:')
        print(f'{dealer.printHand(showOnlyMin=True)}\n')
        isDealersTurn = False
        playAgain = getUserSelectionFromOptions(
          f'Great job {winningPlayerNames}, you win! Want to play again [y/n]?',
          ['y', 'n'])
      else:
        # the dealer continues their turn
        print(f'{dealer.printHand()}\n')
    else:
      print('Looks like we tied! Here is my final hand:')
      print(f'{dealer.printHand()}\n')
      isDealersTurn = False
      playAgain = getUserSelectionFromOptions(
        f'Nice job {winningPlayerNames}, you tied with me! Want to play again [y/n]?',
        ['y', 'n'])
  return playAgain

# play a round of the game
def playRound(players, dealer, deck):
  print('All right, now let\'s play!\n')

  # generate new hands for players and the dealer
  generateAllHands(players, dealer, deck)

  # let each player take their turn
  for player in players:
    doPlayerTurn(player, deck)

  # let the dealer take their turn
  playAgain = doDealerTurn(dealer, deck, players)

  # discard all cards used
  discardAllHands(players, dealer, deck)

  return playAgain

# runs the game of Blackjack
def run():
  # initialize the game
  print('Welcome to Blackjack! My name is Klaus, I’ll be your dealer.')
  numberOfPlayers = getNumericalUserInput('How many players are joining me today?')
  print()
  players = initPlayers(numberOfPlayers)
  numberOfDecks = getNumericalUserInput('How many decks would you like to use?')
  deck = Deck(numberOfDecks)
  dealer = Player('dealer')
  playAgain = 'y'

  # continue the game while the players want to play
  while (playAgain == 'y'):
    playAgain = playRound(players, dealer, deck)

  print('Thanks for playing! I hope you had as much fun as I did!')
