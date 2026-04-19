# import cowsay

# cowsay.cow("Hello world!")

# print(cowsay.char_names)

# cowsay.beavis("he he he he")

# import art

# art.tprint("Hello!")

#from rich.console import Console
#from rich.table import Table
#
#console = Console()
#
#table = Table(title="Список студентів")
#
#table.add_column("Ім'я", style='cyan')
#table.add_column("Проєкт", style='magenta')
#
#table.add_row('Антон', 'Гра')
#table.add_row('Анастасія', 'Чат-бот')
#
#console.print(table)
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from datetime import datetime
import random

console = Console()

history = []
round_num = 1

while True:
    console.clear()

    console.print(
        Panel(
            "[bold yellow]Main menu[/bold yellow]\n\n"
                  "[1] Start game\n"
                  "[2] Game history\n"
                  "[3] Exit",
            border_style="blue",
            title="Menu",
            title_align="center"
        )
    )

    choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])

    if choice == "1":
        console.print("\n[bold magenta]Rock Paper Scissors[/bold magenta]\n")
        console.print("1 - Rock\n2 - Paper\n3 - Scissors")

        player = Prompt.ask("Your choice", choices=["1", "2", "3"])

        moves = {
            "1": "Rock",
            "2": "Paper",
            "3": "Scissors"
        }

        player_move = moves[player]
        computer_move = random.choice(list(moves.values()))

        console.print(f"\n[blue]Computer chose: {computer_move}[/blue]")

        if player_move == computer_move:
            result = "Tie"
            console.print("[yellow]Tie[/yellow]")
        elif (
            (player == "1" and computer_move == "Scissors") or
            (player == "2" and computer_move == "Rock") or
            (player == "3" and computer_move == "Paper")
        ):
            result = "Win"
            console.print("[green]You won![/green]")
        else:
            result = "Loss"
            console.print("[red]You lost![/red]")

        history.append({
            "round": round_num,
            "player": player_move,
            "computer": computer_move,
            "result": result
        })

        round_num += 1

        input("\nPress Enter to return to the menu...")

    elif choice == "2":
        table = Table(title="Game History")

        table.add_column("Round", style="magenta")
        table.add_column("Player", style="white")
        table.add_column("Computer", style="white")
        table.add_column("Result", style="bold magenta")

        wins = 0
        losses = 0
        draws = 0

        for game in history:
            res = game["result"]

            if res == "Win":
                color_res = "[green]Win[/green]"
                wins += 1
            elif res == "Loss":
                color_res = "[red]Loss[/red]"
                losses += 1
            else:
                color_res = "[yellow]Tie[/yellow]"
                draws += 1

            table.add_row(
                str(game["round"]),
                game["player"],
                game["computer"],
                color_res
            )

        console.print(table)

        console.print("\n[bold]Statistics:[/bold]")
        console.print(f"Wins: {wins}")
        console.print(f"Losses: {losses}")
        console.print(f"Draws: {draws}")

        input("\nPress Enter to return to the menu...")

    elif choice == "3":
        console.print("[bold blue]Exiting the game...[/bold blue]")
        break