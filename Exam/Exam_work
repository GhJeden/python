import random

def menu(): # Это меню для игры, где игрок может выбрать начать новую игру, посмотреть историю игр или выйти из игры.
    print("Welcome to Gallow!")
    print("1. Start New Game")
    print("2. Game History")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1": 
        play_game()
    elif choice == "2":
        try:
            with open("gallows_save.txt", "r") as file: 
                history = file.read()
                print("Game History:")
                print(history)
        except FileNotFoundError:
            print("No game history available.")
        menu()
    elif choice == "3":
        print("Thanks for playing!")
        exit()
    else:
        print("Invalid choice. Please try again.")
        menu()
    return choice

def load_dictionary(file_path): # Эта функция загружает слова из файла и возвращает их в виде списка.
    try:
        with open(file_path, "r") as file:
            content = file.read()
            word_list = content.split(", ")
            word_list = [word.strip() for word in word_list]
            return word_list
    except FileNotFoundError:
        print("Error: The file was not found.")
        return []

def get_random_word(): # Эта функция выдает рандомное слово из файла со словами.
    dictionary = load_dictionary("gallows_wordlist.txt")
    if not dictionary:
        print("No words available to choose from.")
        exit()
    return random.choice(dictionary)

def display_gallow(gallow_state): # Эта функция отображает степень виселицы в зависимости от количества оставшихся шансов.
    if gallow_state == 0:
        print("""
         _______
        |       |
        |
        |
        |
        |
        """)
    elif gallow_state == 1:
        print("""
         _______
        |       |
        |       O
        |
        |
        |
        """)
    elif gallow_state == 2:
        print("""
         _______
        |       |
        |       O
        |       |
        |
        |
        """)
    elif gallow_state == 3:
        print("""
         _______
        |       |
        |       O
        |      /|
        |
        |
        """)
    elif gallow_state == 4:
        print("""
         _______
        |       |
        |       O
        |      /|\\
        |
        |
        """)
    elif gallow_state == 5:
        print("""
         _______
        |       |
        |       O
        |      /|\\
        |      /
        |
        """)
    elif gallow_state == 6:
        print("""
         _______
        |       |
        |       O
        |      /|\\
        |      / \\
        |
        """)
    else:
        print("Invalid gallow state.")
        exit()

def save_data(word, guessed_letters, chances, outcome=None): # Это функция сохраняющая данные игры в файл.
    with open("gallows_save.txt", "a") as file:
        file.write(f"Word: {word}\n")
        file.write(f"Guessed letters: {', '.join(guessed_letters)}\n")
        file.write(f"Chances left: {chances}\n")
        if outcome:
            file.write(f"Outcome: {outcome}\n")
        file.write("--------------------\n")

def display_word(word, guessed_letters): # Эта функция отображает слово с угаданными буквами и подчеркиваниями для неугаданных букв.
    display = ""
    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "
    return display.strip()

def play_game(): # Функция начинающая игру.
    word = get_random_word()
    guessed_letters = []
    chances = 6

    while chances > 0:
        print(display_word(word, guessed_letters))
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter. Try again.") # Строка для того чтобы избежать повторного угадывания одной и той же буквы.
            continue

        guessed_letters.append(guess) # Добавляем угаданную букву в список угаданных букв.

        if guess in word:
            print("Good job! That letter is in the word.")
        else:
            chances -= 1
            gallow_state = 6 - chances
            display_gallow(gallow_state)
            print(f"Wrong guess! You have {chances} chances left.")

        if all(letter in guessed_letters for letter in word): # При помощи этих строк мы заканчиваем игру или начинаем новую.
            print(f"Congratulations! You've guessed the word: {word}")
            print("Do you want to save your game? (yes/no)")
            if input().lower() == "yes":
                save_data(word, guessed_letters, chances, "won")
                print("Game saved!")
            print("Do you want to play again? (yes/no)")
            if input().lower() == "yes":
                play_game()
            else:
                print("Thanks for playing!")
                print("Do you want to go back to the menu? (yes/no)")
                if input().lower() == "yes":
                    menu()
                else:
                    exit()
            break
    else:
        print(f"Game over! The word was: {word}")
        print("Do you want to save your game? (yes/no)")
        if input().lower() == "yes":
            save_data(word, guessed_letters, chances, "lost")
            print("Game saved!")
        print("Do you want to play again? (yes/no)")
        if input().lower() == "yes":
            play_game()
        else:
            print("Thanks for playing!")
            print("Do you want to go back to the menu? (yes/no)")
            if input().lower() == "yes":
                menu()
            else:
                exit()

menu()


