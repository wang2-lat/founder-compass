import typer
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from datetime import datetime
import database
import visualize

app = typer.Typer(help="Mental state tracker for startup founders")
console = Console()

@app.command()
def log():
    """Log your daily mental state"""
    console.print("[bold cyan]Daily Check-in[/bold cyan]")
    
    mood = IntPrompt.ask("Mood (1-10, 1=terrible, 10=great)", default=5)
    stress = IntPrompt.ask("Stress level (1-10, 1=calm, 10=overwhelmed)", default=5)
    progress = IntPrompt.ask("Progress feeling (1-10, 1=stuck, 10=crushing it)", default=5)
    note = Prompt.ask("Quick note (optional)", default="")
    
    database.save_log(mood, stress, progress, note)
    console.print("[green]✓ Logged successfully[/green]")

@app.command()
def decide():
    """Decision framework to clarify your thinking"""
    console.print("[bold cyan]Decision Framework[/bold cyan]\n")
    
    decision = Prompt.ask("What decision are you facing?")
    
    console.print("\n[yellow]Let's break it down:[/yellow]")
    worst_case = Prompt.ask("1. What's the worst that could happen?")
    best_case = Prompt.ask("2. What's the best outcome?")
    cost = Prompt.ask("3. What will it cost you (time/money/energy)?")
    regret = Prompt.ask("4. Will you regret NOT doing this in 5 years?")
    gut = Prompt.ask("5. What does your gut say? (yes/no/unsure)")
    
    database.save_decision(decision, worst_case, best_case, cost, regret, gut)
    
    console.print("\n[green]✓ Decision logged[/green]")
    console.print("[dim]Review your past decisions with: founder-compass history[/dim]")

@app.command()
def view(days: int = typer.Option(30, help="Number of days to show")):
    """View your mental state trends"""
    logs = database.get_logs(days)
    
    if not logs:
        console.print("[yellow]No data yet. Start with: founder-compass log[/yellow]")
        return
    
    visualize.show_trends(logs)

@app.command()
def history(limit: int = typer.Option(10, help="Number of entries to show")):
    """View recent logs and decisions"""
    logs = database.get_logs(limit)
    decisions = database.get_decisions(limit)
    
    if logs:
        console.print("\n[bold cyan]Recent Check-ins[/bold cyan]")
        table = Table()
        table.add_column("Date")
        table.add_column("Mood")
        table.add_column("Stress")
        table.add_column("Progress")
        table.add_column("Note")
        
        for log in logs:
            table.add_row(
                log['date'][:10],
                str(log['mood']),
                str(log['stress']),
                str(log['progress']),
                log['note'][:30] if log['note'] else ""
            )
        console.print(table)
    
    if decisions:
        console.print("\n[bold cyan]Recent Decisions[/bold cyan]")
        for d in decisions:
            console.print(f"\n[yellow]{d['date'][:10]}[/yellow]: {d['decision']}")
            console.print(f"  Gut feeling: {d['gut']}")

@app.command()
def stats():
    """Show overall statistics"""
    stats = database.get_stats()
    
    if not stats:
        console.print("[yellow]No data yet[/yellow]")
        return
    
    console.print("\n[bold cyan]Your Stats[/bold cyan]")
    console.print(f"Total check-ins: {stats['total_logs']}")
    console.print(f"Average mood: {stats['avg_mood']:.1f}/10")
    console.print(f"Average stress: {stats['avg_stress']:.1f}/10")
    console.print(f"Average progress: {stats['avg_progress']:.1f}/10")
    console.print(f"Decisions made: {stats['total_decisions']}")

if __name__ == "__main__":
    database.init_db()
    app()
