import random

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

console = Console()

def choose_yes_no(prompt_text, default="no"):
    """Запрашивает у пользователя ответ да/нет с заданным текстом и значением по умолчанию."""
    answer = Prompt.ask(
        f"[bold cyan]{prompt_text}[/]",
        choices=["yes", "no"],
        default=default,
        show_choices=True,
    )
    return answer.lower() == "yes"


def menu():
    """Отображает главное меню игры и обрабатывает выбор пользователя."""
    while True:
        console.clear()
        menu_panel = Panel(
            "[bold white]Guess letters one by one or try the whole word at once![/]",
            title="[bold magenta]GALLOW[/]",
            border_style="bright_blue",
        )
        console.print(menu_panel)

        menu_table = Table.grid(padding=1)
        menu_table.add_column(justify="left")
        menu_table.add_row("[bold green]1[/] - Start New Game")
        menu_table.add_row("[bold green]2[/] - Game History")
        menu_table.add_row("[bold green]3[/] - Add a Word")
        menu_table.add_row("[bold green]4[/] - Exit")
        console.print(menu_table)

        choice = Prompt.ask(
            "Enter your choice",
            choices=["1", "2", "3", "4"],
            default="1",
            show_choices=True,
        )

        if choice == "1":
            play_game()
        elif choice == "2":
            try:
                with open("gallows_save.txt", "r", encoding="utf-8") as file:
                    history = file.read().strip() or "No saved games yet."
            except FileNotFoundError:
                history = "No game history available."

            console.print(Panel(history, title="[bold yellow]Game History[/]", border_style="yellow"))
            Prompt.ask("Press Enter to return to menu", default="")
        elif choice == "3":
            add_word()
        else:
            console.print("[bold green]Thanks for playing![/]")
            raise SystemExit


def load_dictionary(file_path):
    """Загружает список слов из файла и возвращает его как список."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()
            word_list = [word.strip() for word in content.replace("\n", ",").split(",") if word.strip()]
            return word_list
    except FileNotFoundError:
        console.print("[red]Error: The word list file was not found.[/]")
        return []


def get_random_word():
    """Выбирает случайное слово из словаря для игры."""
    dictionary = load_dictionary("gallows_wordlist.txt")
    if not dictionary:
        console.print("[red]No words available to choose from.[/]")
        raise SystemExit
    return random.choice(dictionary).lower()


def add_word():
    """Позволяет пользователю добавить новое слово в словарь."""
    console.clear()
    console.print(
        Panel(
            "[bold white]Add a new word to the game dictionary.[/]",
            title="[bold magenta]Add Word[/]",
            border_style="bright_blue",
        )
    )
    new_word = Prompt.ask("Enter a single new word").strip().lower()
    if not new_word.isalpha():
        console.print("[yellow]Only alphabetic words are allowed. Try again.[/]")
        Prompt.ask("Press Enter to return to menu", default="")
        return

    existing_words = {word.lower() for word in load_dictionary("gallows_wordlist.txt")}
    if new_word in existing_words:
        console.print(f"[yellow]The word '{new_word}' is already in the dictionary.[/]")
        Prompt.ask("Press Enter to return to menu", default="")
        return

    existing_content = ""
    try:
        with open("gallows_wordlist.txt", "r", encoding="utf-8") as file:
            existing_content = file.read().strip()
    except FileNotFoundError:
        existing_content = ""

    with open("gallows_wordlist.txt", "a", encoding="utf-8") as file:
        file.write(new_word if not existing_content else f"\n{new_word}")

    console.print(f"[green]Added '{new_word}' to the dictionary![/]")
    Prompt.ask("Press Enter to return to menu", default="")


def display_gallow(gallow_state):
    """Отображает текущее состояние виселицы в зависимости от количества ошибок."""
    states = [
        """
         _______
        |       |
        |
        |
        |
        |
        """,
        """
         _______
        |       |
        |       O
        |
        |
        |
        """,
        """
         _______
        |       |
        |       O
        |       |
        |
        |
        """,
    """
         _______
        |       |
        |       O
        |      /|
        |
        |
        """,
        """
         _______
        |       |
        |       O
        |      /|\
        |
        |
        """,
        """
         _______
        |       |
        |       O
        |      /|\
        |      /
        |
        """,
        """
         _______
        |       |
        |       O
        |      /|\
        |      / \
        |
        """,
    ]

    if 0 <= gallow_state < len(states):
        console.print(Panel(states[gallow_state], title="[bold red]Gallow[/]", border_style="red"))
    else:
        console.print("[red]Invalid gallow state.[/]")
        raise SystemExit


def save_data(word, guessed_letters, chances, outcome=None):
    """Сохраняет данные игры в файл для истории."""
    with open("gallows_save.txt", "a", encoding="utf-8") as file:
        file.write(f"Word: {word}\n")
        file.write(f"Guessed letters: {', '.join(sorted(set(guessed_letters)))}\n")
        file.write(f"Chances left: {chances}\n")
        if outcome:
            file.write(f"Outcome: {outcome}\n")
        file.write("--------------------\n")


def display_word(word, guessed_letters):
    """Возвращает слово с угаданными буквами и подчеркиваниями для неугаданных."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in word)


def play_game():
    """Запускает основную игру в виселицу."""
    word = get_random_word()
    guessed_letters = []
    chances = 6

    while chances > 0:
        console.clear()
        guessed_display = ", ".join(sorted(set(guessed_letters))) or "None"
        console.print(
            Panel(
                display_word(word, guessed_letters),
                title="[bold green]Word[/]",
                subtitle=f"Chances left: {chances}",
                border_style="green",
            )
        )
        console.print(Panel(f"[cyan]Guessed letters:[/] {guessed_display}", border_style="cyan"))

        guess = Prompt.ask("Guess a letter or the full word").strip().lower()
        if not guess:
            console.print("[yellow]Please type a letter or the full word.[/]")
            continue

        if len(guess) == 1:
            if guess in guessed_letters:
                console.print("[yellow]You already guessed that letter. Try a new one.[/]")
                continue

            guessed_letters.append(guess)
            if guess in word:
                console.print(f"[bold green]Good job![/] '{guess}' is in the word.")
            else:
                chances -= 1
                display_gallow(6 - chances)
                console.print(f"[bold red]Wrong guess![/] You have {chances} chances left.")
        else:
            if guess == word:
                guessed_letters = sorted(set(word))
                console.print("[bold green]Amazing![/] You guessed the whole word in one try!")
                break
            chances -= 1
            display_gallow(6 - chances)
            console.print(f"[bold red]Wrong word guess![/] You have {chances} chances left.")

        if all(letter in guessed_letters for letter in word):
            break

    guessed_display = ", ".join(sorted(set(guessed_letters))) or "None"
    if all(letter in guessed_letters for letter in word):
        console.print(
            Panel.fit(
                f"[bold white]You uncovered the secret word![/]\n\n"
                f"[bold green]{word}[/]\n\n"
                f"[cyan]Guessed letters:[/] {guessed_display}",
                title="[bold bright_green]YOU WON![/]",
                border_style="bright_green",
            )
        )
        if choose_yes_no("Save your game?", default="yes"):
            save_data(word, guessed_letters, chances, "won")
            console.print("[green]Game saved![/]")
    else:
        console.print(
            Panel.fit(
                f"[bold white]The word was:[/] [bold yellow]{word}[/]\n\n"
                f"[cyan]Guessed letters:[/] {guessed_display}\n\n"
                "[red]Better luck next time![/]",
                title="[bold red]GAME OVER[/]",
                border_style="red",
            )
        )
        if choose_yes_no("Save your game?", default="yes"):
            save_data(word, guessed_letters, chances, "lost")
            console.print("[green]Game saved![/]")

    if choose_yes_no("Play again?", default="yes"):
        play_game()
    elif choose_yes_no("Return to the menu?", default="yes"):
        menu()
    else:
        console.print("[bold green]Thanks for playing![/]")
        raise SystemExit


if __name__ == "__main__":
    menu()


