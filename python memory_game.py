import tkinter as tk
import random
from tkinter import messagebox
from playsound import playsound  # Library for playing sounds

class MemoryGame:
    def __init__(self, root, max_attempts=20):
        self.root = root
        self.root.title("Memory Game")
        
        # Set up the cards and game variables
        self.cards = list(range(1, 9)) * 2  # 8 pairs shuffled
        random.shuffle(self.cards)

        self.buttons = []  # Store the interface buttons
        self.selection = []  # Store the selected cards
        self.pairs_found = 0  # Counter for found pairs
        self.attempts = 0  # Counter for attempts made
        self.max_attempts = max_attempts  # Maximum attempts limit

        self.create_buttons()  # Initialize the buttons

    def create_buttons(self):
        """Creates the button grid for the game."""
        for i in range(4):  # 4 rows
            row = []
            for j in range(4):  # 4 columns
                button = tk.Button(
                    self.root, text="?", width=6, height=3, 
                    command=lambda i=i, j=j: self.flip_card(i, j)
                )
                button.grid(row=i, column=j, padx=5, pady=5)  # Add the button to the grid
                row.append(button)
            self.buttons.append(row)  # Add the row to the button matrix

    def flip_card(self, i, j):
        """Handles the card flipping."""
        if len(self.selection) < 2 and self.buttons[i][j]["text"] == "?":
            # Reveal the card value
            self.buttons[i][j]["text"] = str(self.cards[i * 4 + j])
            self.selection.append((i, j))  # Store the selection

            if len(self.selection) == 2:
                self.attempts += 1  # Increment the attempts counter
                self.root.after(1000, self.check_pair)  # Wait 1 second to check the pair

    def check_pair(self):
        """Checks if the two flipped cards form a pair."""
        (i1, j1), (i2, j2) = self.selection  # Get the positions of the selected cards
        if self.cards[i1 * 4 + j1] == self.cards[i2 * 4 + j2]:
            self.pairs_found += 1  # Increment the found pairs counter
        else:
            # Hide the cards again
            self.buttons[i1][j1]["text"] = "?"
            self.buttons[i2][j2]["text"] = "?"

        self.selection = []  # Clear the selection

        # Check if the game has ended
        if self.pairs_found == 8:
            self.victory_message()
        elif self.attempts >= self.max_attempts:
            self.defeat_message()

    def victory_message(self):
        """Displays a victory message."""
        playsound("victory.mp3")  # Play victory sound
        messagebox.showinfo(
            "Victory!", f"Congratulations! You found all pairs in {self.attempts} attempts."
        )
        self.root.quit()  # End the game

    def defeat_message(self):
        """Displays a defeat message."""
        playsound("defeat.mp3")  # Play defeat sound
        messagebox.showinfo(
            "Defeat", f"You reached the limit of {self.max_attempts} attempts! Try again."
        )
        self.root.quit()  # End the game

if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    game = MemoryGame(root, max_attempts=20)  # Initialize the game with a maximum of 20 attempts
    root.mainloop()  # Start the GUI loop
