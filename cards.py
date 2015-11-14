import random

class Deck:

	def __init__(self):
		self.suits = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
		self.nums = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
		self.deck = self.construct_deck()


	def shuffle(self):
		to_shuffle = self.construct_deck()
		new_deck = []
		while len(to_shuffle) > 0:
			random_card = random.choice(to_shuffle)
			to_shuffle.remove(random_card)
			new_deck.append(random_card)
		self.deck = new_deck

	def construct_deck(self):
		new_deck = []
		for suit in self.suits:
			for num in self.nums:
				new_card = Card(suit, num)
				new_deck.append(new_card)
		return new_deck


	def get_next_card(self):
		try:
			return self.deck.pop()
		except IndexError:
			print('No more cards to deal!')

	def verify_deck(self):
		full_deck = self.construct_deck()
		for card in self.deck:
			if card not in full_deck:
				return False
		return True

class Card:

	def __init__(self, suit, num):
		self.suit = suit
		self.num = num

	def __eq__(self, card2):
		return self.suit == card2.suit and self.num == card2.num


if __name__ == '__main__':

	test = Deck()
	assert(len(test.deck) == 52), "Deck is incomplete!"
	for card in test.deck:
		print('Suit: ' + card.suit + ' Num: ' + card.num)

	for i in range(len(test.deck)):
		test.get_next_card()

	test.get_next_card()
	test.shuffle()
	assert(test.verify_deck() == True), "Invalid Deck!"

	for i in range(len(test.deck)):
		card = test.get_next_card()
		print('Suit : ' + card.suit + ' Num: ' + card.num)

	test.shuffle()
	assert(test.verify_deck() == True), "Invalid Deck!"

