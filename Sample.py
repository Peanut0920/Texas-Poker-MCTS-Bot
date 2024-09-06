from Hand import *

start = Card()
start.Shuffle()
p1 = Player(start.cards, "Player1")
bot = Player(start.cards, "Bot")
game_p1 = PokerGame(p1.cards)
game_bot = PokerGame(bot.cards)
betting = Betting()
betting.add_player(p1)
betting.add_player(bot)
print("\n\nFirst Round:")
print("Bot card: ", p1.cards)
print("P1 card: ", bot.cards)
print("Player 1 Hand:", game_p1.evaluate_hand())
print("Bot Hand:", game_bot.evaluate_hand())
print("Player 1 reward:", game_p1.reward())
print("Bot reward:", game_bot.reward())
betting.start_round()
while not betting.all_players_acted():
    current_player = betting.next_player()
    # Example actions
    if not current_player.fold:
        current_player.Raise(300)
        betting.update_pot(300)
betting.end_round()


middle = Community(start.cards)
game_p1 = PokerGame(p1.cards, middle.card)
game_bot = PokerGame(bot.cards, middle.card)
print("\n\nSecond Round:")
print("Bot card: ", game_bot.list)
print("P1 card: ", game_p1.list)
print("Player 1 Hand:", game_p1.evaluate_hand())
print("Bot Hand:", game_bot.evaluate_hand())
print("Player 1 reward:", game_p1.reward())
print("Bot reward:", game_bot.reward())
betting.start_round()
while not betting.all_players_acted():
    current_player = betting.next_player()
    # Example actions
    if not current_player.fold:
        current_player.Raise(300)
        betting.update_pot(300)
betting.end_round()

middle.FourthCard(start.cards)
game_p1 = PokerGame(p1.cards, middle.card)
game_bot = PokerGame(bot.cards, middle.card)
print("\n\nThird Round:")
print("Bot card: ", game_bot.list)
print("P1 card: ", game_p1.list)
print("Player 1 Hand:", game_p1.evaluate_hand())
print("Bot Hand:", game_bot.evaluate_hand())
print("Player 1 reward:", game_p1.reward())
print("Bot reward:", game_bot.reward())
betting.start_round()
while not betting.all_players_acted():
    current_player = betting.next_player()
    # Example actions
    if not current_player.fold:
        current_player.Check()
betting.end_round()

middle.FirthCard(start.cards)
game_p1 = PokerGame(p1.cards, middle.card)
game_bot = PokerGame(bot.cards, middle.card)
print("\n\nFourth Round:")
print("Bot card: ", game_bot.list)
print("P1 card: ", game_p1.list)
print("Player 1 Hand:", game_p1.evaluate_hand())
print("Bot Hand:", game_bot.evaluate_hand())
print("Player 1 reward:", game_p1.reward())
print("Bot reward:", game_bot.reward())
betting.start_round()
while not betting.all_players_acted():
    current_player = betting.next_player()
    # Example actions
    if not current_player.fold:
        current_player.Call(300)
        betting.update_pot(300)
betting.end_round()

print("\n\nFirth Round:")
print(PokerGame.compare_hands(game_p1, game_bot))
