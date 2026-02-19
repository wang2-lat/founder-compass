import plotext as plt
from rich.console import Console

console = Console()

def show_trends(logs):
    if len(logs) < 2:
        console.print("[yellow]Need at least 2 entries to show trends[/yellow]")
        return
    
    logs = list(reversed(logs))
    dates = [log['date'][:10] for log in logs]
    moods = [log['mood'] for log in logs]
    stress = [log['stress'] for log in logs]
    progress = [log['progress'] for log in logs]
    
    console.print("\n[bold cyan]Your Mental State Trends[/bold cyan]\n")
    
    plt.clear_figure()
    plt.plot(dates, moods, label="Mood")
    plt.plot(dates, stress, label="Stress")
    plt.plot(dates, progress, label="Progress")
    plt.title("Mental State Over Time")
    plt.xlabel("Date")
    plt.ylabel("Score (1-10)")
    plt.ylim(0, 11)
    plt.show()
    
    console.print()
