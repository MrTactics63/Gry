import random

def get_user_choice():
    user_choice = input("Wybierz kamień, papier lub nożyce: ").lower()
    while user_choice not in ['kamień', 'papier', 'nożyce']:
        print("Niepoprawny wybór. Spróbuj ponownie.")
        user_choice = input("Wybierz kamień, papier lub nożyce: ").lower()
    return user_choice

def get_computer_choice():
    return random.choice(['kamień', 'papier', 'nożyce'])

def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "Remis!"
    elif (
        (user_choice == 'kamień' and computer_choice == 'nożyce') or
        (user_choice == 'papier' and computer_choice == 'kamień') or
        (user_choice == 'nożyce' and computer_choice == 'papier')
    ):
        return "Wygrałeś!"
    else:
        return "Przegrałeś!"

def play_game():
    print("Witaj w grze kamień-papier-nożyce!")
    
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    
    print(f"Twój wybór: {user_choice}")
    print(f"Wybor komputera: {computer_choice}")
    
    result = determine_winner(user_choice, computer_choice)
    print(result)

if __name__ == "__main__":
    play_game()