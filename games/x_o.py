from os import system
from termcolor import colored

def main():
    clear_screen()
    g_f = [[1,2,3],[4,5,6],[7,8,9]]
    guessed_number = []
    turn = colored("X", "red")
    next_turn = colored("O", "blue")
    turn_time = 0
    while True:
        print(f"it is {turn} turn.")
        print_game_board(g_f)
        finished = True
        location = get_input(turn, g_f, guessed_number)
        g_f[location // 3][location % 3] = turn

        winn = winner(g_f)
        if winn != None:
            break
        
        turn, next_turn = next_turn, turn
        turn_time += 1
        finished = False
        if turn_time == 9:
            print("You are Draw!")
            print_game_board(g_f)
            break

    if finished:
        print(colored("Congrats to", "green"), colored(turn, "red"),colored("!\nYOU WON!", "green"))
        print_game_board(g_f)



def get_input(turn, g_f, guessed_number: list):
    while True:
        try:
            location = int(input(f"Choose a number to place {turn}: ")) - 1
            if 0 <= location <= 8:
                if location not in guessed_number:
                    guessed_number.append(location)
                    clear_screen()
                    return location
                else:
                    clear_screen()
                    print(f"You allready entered {location + 1}!\ntry another number between 1 _ 9.\n")
                    print_game_board(g_f)
                    continue
            else:
                clear_screen()
                print("Enter a number between 1 _ 9 only!\ntry again.\n")
                print_game_board(g_f)
                continue
        except ValueError:
            clear_screen()
            print("Enter a number between 1 _ 9 only!\ntry again.\n")
            print_game_board(g_f)



def winner(g_f: list):
    for i in range(3):
        if g_f[i][0] == g_f[i][1] == g_f[i][2]:
            return True
        elif g_f[0][i] == g_f[1][i] == g_f[2][i]:
            return True
    if g_f[0][0] == g_f[1][1] == g_f[2][2]:
        return True
    elif g_f[0][2] == g_f[1][1] == g_f[2][0]:
        return True
    return None

def clear_screen():
    system("cls")

def print_game_board(g_f):
    print(f"""
{g_f[0][0]}|{g_f[0][1]}|{g_f[0][2]}
{g_f[1][0]}|{g_f[1][1]}|{g_f[1][2]}
{g_f[2][0]}|{g_f[2][1]}|{g_f[2][2]}""")

# if __name__ == '__main__':
#     main()
