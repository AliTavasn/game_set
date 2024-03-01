import games.hangman as hangman
import games.x_o as x_o
from sys import exit
from os import system
from pyfiglet import Figlet
from termcolor import colored


def main():
    clear_screen()
    print(colored("""Hello. Wellcome to this amazing Game Set! I hope you enjoy.
There are two intresting games in here. The "Hangman" game and the "X-O" game.\n""", "green"))
    print(colored("""If you want to play "Hangman" game, enter 1\nif you want to play "X-O" game, enter 2\nif you want to exit the program, enter 3""", "blue"))
 
    while True:
        try:
            game = int(input(colored("Enter 1, 2 or 3: ", "blue")))
            if game == 1:
                clear_screen()
                hang_title = Figlet(font='slant')
                print(colored(hang_title.renderText('Hangman'), "blue"), "\n")
                input(colored("""Welcome to Hangman game! You have to guess my word and you only have 6 chances 
to make a mistake and after that you will lose. Enter any key to continue: """, "green"))
                hangman.main()
                print(colored("""\nIf you want to play again, enter 1\nif you want to play "X-O" game, enter 2\nif you want to exit the program, enter 3""", "green"))
            elif game == 2:
                clear_screen()
                xo_title = Figlet(font='slant')
                print(colored(xo_title.renderText('X - O'), "blue"), "\n")
                input(colored("""Welcome to X_O game! This is a 2 player game and you should play it with
your friends. The rules of this game are pretty clear. Enter any key to continue: """, "green"))
                x_o.main()
                print(colored("""\nIf you want to play again, enter 2\nIf you want to play "Hangman" game, enter 1\nif you want to exit the program, enter 3""", "green"))
            elif game == 3:
                exit()
            else:
                clear_screen()
        except ValueError:
            clear_screen()
        


def clear_screen():
    system("cls")



if __name__ == "__main__":
    main()