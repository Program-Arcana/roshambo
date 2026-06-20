import random
import time
import tkinter as tk
from tkinter import messagebox


class GUI:
    def __init__(self):
        # Style Attributes
        self.font = "Calibri"
        self.name_size = 20
        self.choice_size = 40
        self.button_size = 40
        # Setup Root Window
        self.root = tk.Tk()
        self.root.title("Roshambo")
        self.center_root()
        # Icon displays for player choices
        self.user_choice = None
        self.computer_choice = None
        # Game Stats/Assets
        self.choices = ["🪨", "📝", "✂️"]
        self.user_score = 0
        self.computer_score = 0
        self.best_of = 3
        # Additional widgets/setup
        self.user_score_label = None
        self.computer_score_label = None
        self.game_text = None # Displaying game text (outcome of each round)
        self.choice_frame = None # Choice buttons (disabled when updating score)
        self.setup_frames()

    def center_root(self) -> None:
        """
        Centers the root window using the screen size and window size
        """
        # Screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        # Window dimensions
        window_width = 495
        window_height = 440
        # (x,y) starts at top left of window (0, 0)
        # x increases moving right, decreases moving left
        # y increases moving down, decreases moving up
        x = screen_width / 2 - window_width / 2 # position top left corner's x at this x
        y = screen_height / 2 - window_height # position top left corner's y at a smaller y (otherwise window too low)
        self.root.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y)) # Adds x and y offsets to window dims
        self.root.resizable(width=False, height=False) # Prevent window from being resizable

    def setup_frames(self) -> None:
        """
        Sets up the frames for each component of the GUI window
        """
        self.setup_text_frame() # Text at top of the window (not program title)
        self.setup_user_frame() # Everything inside the "You" section
        self.setup_vs_frame() # The "vs" text in the middle of the window
        self.setup_computer_frame() # Everything inside the "Computer" section
        self.setup_choice_frame() # The button choices for the user to pick at the bottom of window

    def setup_text_frame(self) -> None:
        """
        Sets up the game text frame (sets max score and displays round information)
        """
        text_frame = tk.Frame(self.root)
        text_frame.grid(row=0, column=0, columnspan=3)
        self.game_text = tk.Label(text_frame, text=f"Best of {self.best_of}", font=(self.font, 30, "bold"), justify="center")
        self.game_text.grid(row=0, column=0, columnspan=3)

    def setup_user_frame(self) -> None:
        """
        Sets up the user side of the screen
        """
        user_frame = tk.Frame(self.root, bd=10, relief="ridge")
        user_frame.grid(row=1, column=0)
        user_label = tk.Label(user_frame, text="You", font=(self.font, 20, "bold"), justify="center")
        user_label.grid(row=0, column=0)
        self.user_score_label = tk.Label(user_frame, text=f"Score: {self.user_score}", font=(self.font, self.name_size), justify="center")
        self.user_score_label.grid(row=1, column=0)
        self.user_choice = tk.Label(user_frame, text="", width=5, height=2, font=(self.font, self.choice_size, "bold"), justify="center")
        self.user_choice.grid(row=2, column=0)

    def setup_vs_frame(self) -> None:
        """
        Sets up the vs (middle) of the screen
        """
        vs_frame = tk.Frame(self.root)
        vs_frame.grid(row=1, column=1)
        vs_label = tk.Label(vs_frame, text="VS", font=(self.font, 20, "bold"), justify="center")
        vs_label.grid(row=0, column=0, padx=20)

    def setup_computer_frame(self) -> None:
        """
        Sets up the computer side of the screen
        """
        computer_frame = tk.Frame(self.root, bd=10, relief="ridge")
        computer_frame.grid(row=1, column=2)
        computer_label = tk.Label(computer_frame, text="Computer", font=(self.font, self.name_size, "bold"), justify="center")
        computer_label.grid(row=0, column=0)
        self.computer_score_label = tk.Label(computer_frame, text=f"Score: {self.computer_score}", font=(self.font, 20), justify="center")
        self.computer_score_label.grid(row=1, column=0)
        self.computer_choice = tk.Label(computer_frame, text="", width=5, height=2, font=(self.font, self.choice_size, "bold"), justify="center")
        self.computer_choice.grid(row=2, column=0)

    def setup_choice_frame(self) -> None:
        """
        Sets up the choice frame and the widgets inside to let user pick their choice
        """
        self.choice_frame = tk.Frame(self.root, bd=10, relief="groove")
        self.choice_frame.grid(row=2, column=0, columnspan=3, pady=10)
        choice_text = tk.Label(self.choice_frame, text="Pick One:", font=(self.font, 20, "bold"), justify="center")
        choice_text.grid(row=0, column=0, columnspan=3)
        rock_button = tk.Button(self.choice_frame, text=self.choices[0], font=(self.font, self.button_size),
                                command=lambda:self.update_score(self.choices[0]))
        rock_button.grid(row=1, column=0, padx=10, pady=2)
        paper_button = tk.Button(self.choice_frame, text=self.choices[1], font=(self.font, self.button_size),
                                 command=lambda:self.update_score(self.choices[1]))
        paper_button.grid(row=1, column=1, padx=10, pady=2)
        scissors_button = tk.Button(self.choice_frame, text=self.choices[2], font=(self.font, self.button_size),
                                    command=lambda: self.update_score(self.choices[2]))
        scissors_button.grid(row=1, column=2, padx=10, pady=2)

    def disable_choices(self) -> None:
        """
        Disable all the choice buttons
        """
        for widget in self.choice_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="disabled")

    def enable_choices(self) -> None:
        """
        Enable all the choice buttons
        """
        for widget in self.choice_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(state="normal")

    def update_with_delay(self) -> None:
        """
        Update all widgets, then delays all code after this
        """
        self.root.update()  # Update the user choice label immediately instead of until next loop
        time.sleep(1)  # Delay the results (FOR SUSPENSE)

    def update_score(self, user_choice) -> None:
        """
        Updates the score of the user and computer given their choices
        :param user_choice: the user's choice in the game
        """
        self.disable_choices() # Prevent buttons from being spammed and lagging out the program
        self.clear() # Clear the labels revealing the results and player choices
        self.user_choice.config(text=user_choice)
        self.update_with_delay()
        self.computer_choice.config(text=random.choice(self.choices))
        self.update_with_delay()
        user_choice = self.user_choice.cget("text")
        computer_choice = self.computer_choice.cget("text")
        if user_choice == computer_choice:
            self.game_text.config(text="You Tied", fg="#8B8000")  # yellow text
        else:
            if user_choice == self.choices[0] and computer_choice == self.choices[2] or \
                    user_choice == self.choices[2] and computer_choice == self.choices[1] or \
                    user_choice == self.choices[1] and computer_choice == self.choices[0]:
                self.game_text.config(text=f"You Won!", fg="green")
                self.user_score += 1
                self.user_score_label.config(text=f"Score: {self.user_score}")
            else:
                self.game_text.config(text=f"You Lost", fg="red")
                self.computer_score += 1
                self.computer_score_label.config(text=f"Score: {self.computer_score}")
        self.root.update() # Prevent messagebox from popping up before score label updates
        if self.game_over(): # Check if either player has reached the best of 3
            self.play_again()
        else:
            self.enable_choices()

    def game_over(self) -> bool:
        """
        Checks if the current game is over
        :return: True if the max score has been reached, otherwise False
        """
        return self.user_score == self.best_of - 1 or self.computer_score == self.best_of - 1

    def reset(self) -> None:
        """
        Resets the game when the user wants to play again
        """
        self.game_text.config(text="Best of 3", fg="black")
        self.user_choice.config(text="")
        self.computer_choice.config(text="")
        self.user_score = 0
        self.computer_score = 0
        self.user_score_label.config(text=f"Score: {self.user_score}")
        self.computer_score_label.config(text=f"Score: {self.computer_score}")
        self.enable_choices()

    def clear(self) -> None:
        """
        Only clear the game display, DOESN'T RESET SCORES!
        """
        self.game_text.config(text="...", fg="black")
        self.user_choice.config(text="")
        self.computer_choice.config(text="")

    def play_again(self) -> None:
        """
        Prompt the user and ask them if they want to play again
        """
        if self.user_score > self.computer_score:
            message = "You Win The Game!"
        else:
            message = "You Lose The Game..."
        play_choice = messagebox.askyesno("Game Over", f"{message}\nPlay Again?")
        if play_choice:
            self.reset()
        else:
            exit()

