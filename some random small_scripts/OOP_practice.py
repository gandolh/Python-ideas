from random import choice
posible_values = ['A'] + list(range(2, 11)) + ['J', 'Q', 'K']
symbols = ['inima_rosie', 'inima_neagra', 'trefla', 'romb']


class Card:
    def __init__(self, value, symbol):
        self.value = value
        self.symbol = symbol


class Deck:
    def __init__(self, *cards):
        self.cards = list(cards)

    def shuffle(self):
        new_cards = []
        for i in range(len(self.cards)):
            new_cards.append(choice(self.cards))
            self.delete(new_cards[i])
        self.cards = new_cards

    def add(self, card):
        if (type(card)==Card and card.value in posible_values) and (card.symbol in symbols):
            # paranteze pentru eleganta
            ok = 1
            for card_temp in self.cards:

                if (card.value == card_temp.value) and (card.symbol == card_temp.symbol):
                    ok = 0
                    break
            if ok:
                self.cards.append(card)
                return 1
            else: 
                # print('Duplicate.')
                return -1
        else: 
            # print('invalid type')
            return -2

    def delete(self, card):
    	try:
    		self.cards.index(card)
    		self.cards.remove(card)
    	except ValueError:
            # print('Cannot remove this Card.')
            return -1


def CreateFullDeck():
	deck= Deck()
	for i in symbols:
		for j in posible_values:
			deck.add(Card(j,i))
	return deck

if __name__ == '__main__':

    deck = Deck()
    for i in range(10):
        deck.add(Card(posible_values[i], symbols[0]))
        # deck.add(Card(choice(posible_values),choice(symbols)))
    deck.shuffle()
    error=deck.add(2)
    if error==-1:
        print('Duplicate')
    elif error==-2:
        print('invalid type')
    error=deck.delete(2)
    if error==-1:
        print('Cannot remove this Card.')
    for card in deck.cards:
        print(card.value, card.symbol)
    print('='*100)
    deck1=CreateFullDeck()
    for card in deck1.cards:
    	print(card.value, card.symbol)


