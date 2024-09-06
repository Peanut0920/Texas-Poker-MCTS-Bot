import tkinter as tk
from PIL import Image, ImageTk
from Hand import *
from MCTS import *

STYLE = {
    'width': 10,
    'height': 3,
    'bg': '#333333',
    'fg': 'white',
    'activebackground': '#555555',
    'activeforeground': 'white',
    'borderwidth': 0,
    'font': ('Helvetica', 12, 'bold')
}
class PokerGUI:
    def __init__(self, root):
        self.root = root
        self.reveal_stage = 0
        self.revealed_community_cards = []
        self.root.title("Texas Hold'em Poker")
        self.set_background('Image/background.png')
        self.root.attributes('-fullscreen', True)
        self.loading_label = tk.Label(root, text="", font=('Helvetica', 12, 'bold'))
        self.create_buttons()
        self.card_back_image = ImageTk.PhotoImage(Image.open("Image/Back.png").resize((100, 150), Image.LANCZOS))
        self.display_card((self.card_back_image, None, None), x=1200, y=100)
        self.display_card((self.card_back_image, None, None), x=1195, y=95)
        self.game_init()
        self.display_all(self.p1.cards + self.middle.card + self.bot.cards)

    def create_buttons(self):
        # Button styles
        button_style = {
            'width': 10,
            'height': 3,
            'bg': '#333333',
            'fg': 'white',
            'activebackground': '#555555',
            'activeforeground': 'white',
            'borderwidth': 0,
            'font': ('Helvetica', 12, 'bold')
        }

        # Exit button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit, **STYLE)
        self.exit_button.place(relx=1.0, rely=1.0, anchor='se', x=-1400, y=-50)

        self.reveal_button = tk.Button(self.root, text="Reveal Cards", command=self.reveal_next, **STYLE)
        self.reveal_button.place(relx=1.0, rely=1.0, anchor='se', x=-1000, y=-50)

        # Call button
        self.call_button = tk.Button(self.root, text="Call", command=self.call_action, **STYLE)
        self.call_button.place(relx=1.0, rely=1.0, anchor='se', x=-150, y=-50)

        # Raise button
        self.raise_button = tk.Button(self.root, text="Raise", command=self.raise_action, **STYLE)
        self.raise_button.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-50)

        # Check button
        self.check_button = tk.Button(self.root, text="Check", command=self.check_action, **STYLE)
        self.check_button.place(relx=1.0, rely=1.0, anchor='se', x=-280, y=-50)

        # Fold button
        self.fold_button = tk.Button(self.root, text="Fold", command=self.fold_action, **STYLE)
        self.fold_button.place(relx=1.0, rely=1.0, anchor='se', x=-410, y=-50)

    def enable_button(self):
        print("Enable button")
        self.reveal_button.config(state=tk.NORMAL)
        self.call_button.config(state=tk.NORMAL)
        self.raise_button.config(state=tk.NORMAL)
        self.fold_button.config(state=tk.NORMAL)
        self.check_button.config(state=tk.NORMAL)

    def disable_button(self):
        print("Disable button")
        self.reveal_button.config(state=tk.DISABLED)
        self.call_button.config(state=tk.DISABLED)
        self.raise_button.config(state=tk.DISABLED)
        self.fold_button.config(state=tk.DISABLED)
        self.check_button.config(state=tk.DISABLED)

    def call_action(self):
        self.p1.Call(100)
        print("Call action")

    def raise_action(self):
        # Create and display the scale widget for raise amount
        self.raise_scale = tk.Scale(self.root, from_=1000, to=0, orient=tk.VERTICAL, length=300,
                                    font=('Helvetica', 10), bg='#333333', fg='white',
                                    highlightbackground='#333333', troughcolor='#555555',
                                    tickinterval=100, resolution=10)
        self.raise_scale.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-210)

        # Confirm button
        self.confirm_button = tk.Button(self.root, text="Confirm", command=self.confirm_raise,
                                        width=10, height=2, bg='#333333', fg='white',
                                        activebackground='#555555', activeforeground='white',
                                        borderwidth=0, font=('Helvetica', 10, 'bold'))
        self.confirm_button.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-130)

    def confirm_raise(self):
        raise_amount = self.raise_scale.get()
        self.p1.Raise(raise_amount)
        print(f"Raise action with amount: {raise_amount}")
        self.raise_scale.destroy()  # Remove the scale widget after confirming
        self.confirm_button.destroy()  # Remove the confirm button after confirming

    def check_action(self):
        self.p1.Check()
        print("Check action")

    def fold_action(self):
        self.p1.Fold()
        print("Fold action")

    def set_background(self, image_path):
        bg_image = Image.open(image_path)
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(self.root, image=bg_photo)
        bg_label.image = bg_photo  # Keep a reference to avoid garbage collection
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def game_init(self):
        self.initial_state = "initial"
        self.desk = Card()
        self.desk.Shuffle()
        self.p1 = Player(self.desk.cards, "Player1")
        self.bot = Player(self.desk.cards, "Bot")
        self.betting = Betting()
        self.mcts = MCTS(player_cards=self.bot.cards, community_cards=[], length=5, iterations=10, threshold=5)
        self.betting.add_player(self.p1)
        self.betting.add_player(self.bot)
        self.middle = Community(self.desk.cards)
        self.middle.FourthCard(self.desk.cards)
        self.middle.FirthCard(self.desk.cards)

    def bot_mechanic(self):
        self.mcts = MCTS(player_cards=self.bot.cards, community_cards=self.revealed_community_cards, iterations=100,
                         threshold=5)
    def CardImage(self, cards):
        card_images = []
        for card in cards:
            suit, rank = card
            image = f"Image/{rank}{suit}.png"
            card_image = Image.open(image)
            card_image = card_image.resize((100, 150), Image.LANCZOS)  # Resize the image to 100x150 pixels
            card_photo = ImageTk.PhotoImage(card_image)
            card_images.append((card_photo, suit, rank))
        return card_images

    def display_card(self, card, x, y):
        card_photo, rank, suit = card
        card_label = tk.Label(self.root, image=card_photo)
        card_label.image = card_photo
        card_label.place(x=x, y=y)
        return card_label

    def animate_card(self, card_label, start_pos, end_pos, duration=1000):
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        delta_x = (end_x - start_x) / duration
        delta_y = (end_y - start_y) / duration

        for i in range(duration):
            new_x = start_x + delta_x * i
            new_y = start_y + delta_y * i
            self.root.after(i, lambda x=new_x, y=new_y: card_label.place(x=x, y=y))

    def reveal_card(self, card_label, card_image, card_info):
        card_label.config(image=card_image)
        card_label.image = card_image
        self.revealed_community_cards.append(card_info)

    def reveal_next(self):
        reveal_order = [
            [0, 1],  # Own 2 cards
            [2, 3, 4],  # 3 middle cards
            [5],  # 1 middle card
            [6],  # Last middle card
            [7, 8]  # Opponent's cards
        ]

        if self.reveal_stage < len(reveal_order):
            for index in reveal_order[self.reveal_stage]:
                self.reveal_card(self.card_labels[index], self.card_images[index][0], self.card_images[index][1:])
            self.reveal_stage += 1
            self.bot_mechanic()

    def display_all(self, allcards):
        card_images = self.CardImage(allcards)
        positions = [
            (600, 550), (750, 550),  # Player's cards
            (375, 300), (525, 300), (675, 300), (825, 300), (975, 300),  # Community cards
            (600, 50), (750, 50)  # Opponent's cards
        ]
        self.card_labels = [self.display_card((self.card_back_image, None, None), *pos) for pos in positions]
        self.card_images = card_images
        self.animate_cards(positions)

    def animate_cards(self, positions):
        start_pos = (1200, 100)  # Starting position for the animation
        for i, pos in enumerate(positions):
            card_label = self.card_labels[i]
            self.animate_card(card_label, start_pos, pos, duration=500 + i * 100)

    def play_round(self):
        while self.betting.round < 5:
            self.betting.start_round()
            while not self.betting.all_players_acted():
                current_player = self.betting.next_player()
                print(current_player.name," turn:")
                if current_player.name == "Player1":
                    self.enable_button()
                    while not (self.p1.check or self.p1.raisecall or self.p1.call):
                        self.root.update()
                        self.show_loading_message("You Turn", x=1000, y=50)
                    self.hide_loading_message()

                    while not self.bot_action():
                        self.root.update()
                        self.show_loading_message("Loading and Reacting.", x=675, y=300)
                        self.show_loading_message("Loading and Reacting..", x=675, y=300)
                        self.show_loading_message("Loading and Reacting...", x=675, y=300)
                    self.hide_loading_message()
                    self.disable_button()
                else:
                    self.bot_action()
                self.hide_loading_message()
            self.reveal_next()
            self.betting.end_round()
            self.betting.round += 1

    def show_loading_message(self, message, x, y):
        self.loading_label.config(text=message)
        self.loading_label.place(x=x,y=y)
        self.root.update()

    def hide_loading_message(self):
        self.loading_label.config(text="")
        self.root.update()
    def bot_action(self):
        print("Loading and Reacting")
        if self.initial_state == "initial":
            action = self.mcts.make_action(self.initial_state)
        else:
            action = self.mcts.continue_round(self.initial_state, self.betting.pot, self.betting.current_bet)

        if action == "call":
            self.initial_state = "call"
            self.bot.Call(p1.bet_amount)
            self.betting.update_pot(p1.bet_amount)
        elif action == "raise":
            self.initial_state = "raise"
            new_bet = self.mcts.raise_bet(self.betting.pot, self.betting.current_bet)
            self.bot.Raise(new_bet)
            self.betting.update_pot(new_bet)
        elif action == "check":
            self.initial_state = "check"
            self.bot.Check()
        elif action == "fold":
            self.initial_state = "fold"
            self.bot.Fold()
        return True

if __name__ == "__main__":
    root = tk.Tk()
    gui = PokerGUI(root)
    gui.play_round()
    root.mainloop()
