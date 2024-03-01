import random
import os 
from termcolor import colored


def main():
    clear_screen()
    pcword = select_word()
    gussword = len(pcword) * "-"
    print_word(gussword)
    false_letter = []
    while True:
        gussletter = input("Guess a letter: ").lower()
        clear_screen()
        if check_input(gussletter, gussword):
            if gussletter in gussword:
                print(f"You guessed '{gussletter}' before! try another one.\n")
                print_word(gussword)
            elif gussletter in pcword:
                print(f"'{gussletter}' is correct! keep going.\n")
                letterind = 0
                for i in range(pcword.count(gussletter)):
                    letterind = pcword.index(gussletter,letterind , len(pcword) + 1)
                    gussword = gussword[:letterind] + gussletter + gussword[letterind + 1:]
                    letterind += 1
                print_word(gussword)
                if pcword == gussword:
                    clear_screen()
                    print(colored("\nCongrats! You guess the word.\nYOU WON!\n", "green"))
                    print_word(gussword)
                    break
            else:
                print(f"'{gussletter}' is not in my word! try again.\n")
                print_word(gussword)
                if gussletter not in false_letter:
                    false_letter.append(gussletter)
        print_false_letter(false_letter)
        if len(false_letter) >= 6:
            clear_screen()
            print(colored("\nGame Over!\nYou had 6 mistakes\n", "red"))
            print_word(gussword)
            print(f"\nThe word is '"+ colored(pcword, "green") + "'")
            break


def select_word():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, 'Random_words.txt')
    with open(file_path, 'r') as file:
        words = file.readlines()
    return random.choice(words).strip().lower()


def print_false_letter(false_letter):
    for i in range(len(false_letter)):
        if i == 0:
            print(colored(false_letter[i], "red"), end = "")
        else:
            print(",", colored(false_letter[i], "red"), end = "")
    print()


def check_input(gussletter, gussword):
    if len(gussletter) != 1:
        print("you should guess exactly 1 character!\ntry again.\n")
        print_word(gussword)
        return False
    elif not gussletter.isalpha():
        print("you should guess an alphabet character!\ntry again.\n")
        print_word(gussword)
        return False
    else:
        return True


def print_word(gussword):
    for leter in gussword:
        if leter != "-":
            print(colored(leter, "green"), end = "")
        else:
            print("-", end = "")
    print()

def clear_screen():
    os.system("cls")


# if __name__  == "__main__":
#     main()
 