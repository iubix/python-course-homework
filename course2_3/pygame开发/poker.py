import random

#一张牌
class Poker_card:

    NUMS =  ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    FACES = ['梅花', '方片', '红桃', '黑桃']

    def __init__(self, num, face) -> None:
        self.num = num
        self.face = face

    def __str__(self) -> str:
        return f'{self.face}{self.num}'
    
#手牌(13张)
class Poker_hand:
    def __init__(self) -> list:
        self.cards = []

    def __str__(self) -> str:
        
        res = ''
        for card in self.cards:
            res += str(card) + ' '
        return res

#牌桌(52张)
class Poker_deck(Poker_hand):
    
    def __init__(self) -> None:
        super().__init__()

    def gen(self):
        
        for num in Poker_card.NUMS:
            for face in Poker_card.FACES:
                self.cards.append(Poker_card(num, face))

    def __str__(self) -> str:
        return f'{self.cards}'

    def shuffle(self):
        random.shuffle(self.cards)
    
    def shot(self, hands, ncards = 13):
        
        for i in range(ncards):
            for hand in hands:
                
                if self.cards:
                    hand.cards.append(self.cards.pop())
                else:
                    print('no cards')

if __name__ == '__main__':
    
    #初始化牌桌
    deck = Poker_deck()
    deck.gen()
    deck.shuffle()
    
    #初始化选手
    hands = [Poker_hand() for i in range(4)]

    #发牌
    deck.shot(hands)

    #输出选手的手牌
    for id, hand in enumerate(hands):
        print(f'牌手{id+1}', end = ':')
        print(hand)
        

    
    


    