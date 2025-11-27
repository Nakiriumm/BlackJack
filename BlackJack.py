'''
    turtle_BJ.py (aka. version 1.1) brewed by KunToto@MikeLabDotNet [August 2024]
'''
import random, time
#import turtle

class Card():
    ''' Card(): create a card object. To create a deck, try \\Card.test_Card()\\! '''
    symbols = {"D":"♦", "C":"♣", "H":"♥", "S":"♠"}
    def __init__(self, name, suit):
        self.name = name
        self.suit = suit
    def get_name(self):
        return self.name
    def get_suit(self):
        return self.suit
    def __repr__(self):
        return f"{self.name}{Card.symbols[self.suit]}"
    def test_Card():
        Names = ['A',2,3,4,5,6,7,8,9,'T','J','Q','K']
        Suits = ['D','C','H','S']
        deck = [Card(str(n), s) for s in Suits for n in Names]
        random.shuffle(deck)
        res = [str(card) for card in deck]
        return ' '.join(res)
    def render(self, x, y, color='blue', RENDER=False):
        ''' วาดไพ่ด้วยเต่า '''
        if not RENDER:
            return None

class Deck:
    ''' Deck(): สร้างสำรับไพ่ '''
    Names = ['A',2,3,4,5,6,7,8,9,'T','J','Q','K']
    Suits = ['D','C','H','S']
    def __init__(self):
        Names, Suits = Deck.Names, Deck.Suits
        self.cards = [Card(str(n), s) for s in Suits for n in Names]
    def shuffle(self):
        random.shuffle(self.cards)
    def get_card(self):
        return self.cards.pop()
    def set_cards(self, cards):
        self.cards = cards
    def reset(self, n=1):
        Names, Suits = Deck.Names, Deck.Suits
        self.cards = [Card(str(n), s) for s in Suits for n in Names]
        for i in range(n):
            self.shuffle()
    def __repr__(self):
        res = [str(x) for x in self.cards]
        return ' '.join(res)

def preamble(RENDER=False):
    ''' จัดการ environment ในการวาดเต่า '''
    if not RENDER:
        return None

def test_turtle_deck(RENDER=False):
    ''' ไว้ตรวจสอบเต่าวาดไพ่ ฟังชัน Card.render() '''
    preamble(RENDER)
    # create a deck f card
    deck = Deck()
    # shuffle deck
    deck.reset()
    print(deck)
    # render n cards (back) in a row
    nbOfCards = 5
    start_x = -250
    for x in range(nbOfCards):
        card = Card('', '')
        card.render(start_x + x*125, 175, 'orange', RENDER=True)
    time.sleep(1)
    # re-render n cards in a row
    start_x = -250
    for x in range(nbOfCards):
        card = deck.get_card()
        card.render(start_x + x*125, 175, RENDER=True)
    print('Done..')

def createVirtualDeck(s='K♣ Q♠ A♣ 3♥ 2♠ 6♥ 8♥ 9♥ J♠ 4♦ 2♥ 9♠'):
    dd = s.split()
    res = []
    suit = {'♦':'D','♣':'C','♥':'H','♠':'S'}
    for d in dd:
        card = Card(d[0], suit[d[1]])
        res.append(card)
    deck = Deck()
    deck.set_cards(res)
    return deck

def card_eval(card):
    if card.get_name() == 'T' or card.get_name() == 'J' or card.get_name() == 'Q' or card.get_name() == 'K':
        return 10
    elif card.get_name() == 'A':
        return 11
    else:
        return int(card.get_name())

class myCard:
    def __init__(self):
        self.cards = []
    def hit(self, deck):
        self.cards.append(deck.get_card())
    def score_cal(self):
        score, aces = 0, 0
        for card in self.cards:
            val = card_eval(card)
            score += val
            if val == 11:
                aces += 1
        while score > 21 and aces > 0:
            score -= 10
            aces -= 1
        return score
    def done(self):
        if self.score_cal() == 21 or len(self.cards) == 5:
            return True
        return False

def pc_current_hand(computer, displayed, card_hid=True):
    if card_hid:
        return f'{displayed:>9}: O{computer.cards[0].symbols[computer.cards[0].suit]} {' '.join([str(card) for card in computer.cards[1:]]):<11}  -> {computer.score_cal()-card_eval(computer.cards[0])}'
    else:
        return f'{displayed:>9}: {' '.join([str(card) for card in computer.cards]):<14}  -> {computer.score_cal()}'
    
def pl_current_hand(player, displayed):
    return f'{displayed:>9}: {' '.join([str(card) for card in player.cards]):<14}  -> {player.score_cal()}'

def auto_play(computer, player, deck, displayed):
    while True:
        if len(computer.cards) == 5:
            break
        elif player.done() and computer.score_cal() < 21:
            computer.hit(deck)
        elif computer.score_cal() < 17 or computer.score_cal() < player.score_cal() and player.score_cal() <= 21:
            computer.hit(deck)
        elif computer.score_cal() > 15 and player.score_cal() > 21:
            break
        else:
            break

    print(pc_current_hand(computer, displayed, card_hid=False))



def play(player1='Computer', player2='Player', d=None, RENDER=False):
    print('Welcome to Nakirium\'s BlackJack Casino.')
    preamble(RENDER)
    # create a deck of cards
    if d==None:
        deck = Deck()
        deck.reset()
    else:
        #----------------------------- virtual deck
        #d = 'A♦ A♥ 3♥ 4♣ 4♥ 7♣ 5♣ 6♦ A♠'
        deck = createVirtualDeck(d)
    #----------------------
    #print(deck) # for DEBUG
    #----------------------

    player = myCard()
    pc = myCard()
    pc.hit(deck)
    player.hit(deck)
    pc.hit(deck)
    player.hit(deck)

    print(pc_current_hand(pc, player1, card_hid=True))
    print(pl_current_hand(player, player2))
    moves = 0

    while True:
        if moves == 3 or player.score_cal() >= 21:
            break
        choice = input('Draw another card (y/n): ')
        choice = choice.lower()

        if choice == 'y':
            player.hit(deck)
            print(pl_current_hand(player, player2))
            moves += 1

        else:
            break
    
    print('+++++++++++++++++++++++++++++++++')

    auto_play(pc, player, deck, player1)
    print(pl_current_hand(player, player2))

    p1score = pc.score_cal()
    p2score = player.score_cal()
    p1count = len(pc.cards)
    p2count = len(player.cards)

    print('++++++++++++++++++++++++++++++++++++++++++++++++++')

    if (p1score == 21 and p1count == 2 and p2count == 5) or (p2score == 21 and p2count == 2 and p1count == 5):
        res = "Draw!"
    elif p1count == 5 and p1score <= 21 and p2count == 5 and p2score <= 21:
        res = 'Draw!'
    elif p1count == 5 and p1score <= 21:
        res = f'{player1} wins.'
    elif p2count == 5 and p2score <= 21:
        res = f'{player2} wins.'

    elif p1score > 21:
        res = f'{player2} wins.'
    elif p2score > 21:
        res = f'{player1} wins.'

    elif p1score > p2score:
        res = f'{player1} wins.'
    elif p1score < p2score:
        res = f'{player2} wins.'
    else:
        res = 'Draw!'

    print(res)

    print('++++++++++++++++++++++++++++++++++++++++++++++++++')

## main begins here
def testcase01():
    random.seed(2)
    play()
def testcase02():
    random.seed(16)
    play()
def testcase03():
    random.seed(30)
    play()
def testcase04():
    s = 'K♣ Q♠ A♣ 3♥ 2♠ 6♥ 8♥ 9♥ J♠ 4♦ 2♥ 9♠'
    play('Toto', 'Tutu', d=s)

def testcase05():
    s = 'A♣ 3♥ 2♠ T♥ 8♥ A♠ A♦ 2♥ 3♠'
    play(d=s)
def testcase06():
    s = '4♠ A♥ A♣ 3♥ 2♠ 4♥ 5♥ A♠ A♦ 2♥ 3♠'
    play(d=s)
def testcase07():
    s = '4♠ A♥ A♣ 3♥ 2♠ 4♥ 5♥ A♠ A♦ 2♥ T♠'
    play(d=s)
def testcase08():
    s = '4♠ A♥ A♣ 3♥ 2♠ 4♥ 5♥ A♠ A♦ Q♥ 3♠'
    play(d=s)
def testcase09():
    s = '5♠ A♥ A♣ 8♥ J♠ 4♥ 5♥ A♠ A♦ 2♥ 3♠'
    play(d=s)
def testcase10():
    s = 'A♣ 3♦ A♦ A♥ 3♥ 4♣ 4♥ 7♣ 3♣ 2♦ A♠'
    play(d=s)
#------------------------------------------
q = int(input())
if q==1:
    testcase01()
elif q==2:
    testcase02()
elif q==3:
    testcase03()
elif q==4:
    testcase04()
elif q==5:
    testcase05()
elif q==6:
    testcase06()
elif q==7:
    testcase07()
elif q==8:
    testcase08()
elif q==9:
    testcase09()
elif q==10:
    testcase10()
