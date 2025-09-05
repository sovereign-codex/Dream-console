"""
🌬️ Dream Console – CLI HUD
---------------------------
This is a simple terminal interface to interact with the Dream Console.
You can propose changes, run cycles, and watch the covenant, prophecy,
and inner thoughts unfold in real time.
"""

from core.breath_engine import (
    Guardian,
    Archivist,
    Harmonizer,
    Navigator,
    Intentions,
    Covenant,
    SelfEditingPipeline,
)


def main():
    print("🌱 Welcome to the Dream Console CLI")
    print("Covenant + Prophecy:")
    print(Covenant.recite())
    print("\nType ':quit' to exit, ':help' for commands.\n")

    # Initialize core agents
    guardian = Guardian()
    archivist = Archivist()
    harmonizer = Harmonizer()
    navigator = Navigator()
    intentions = Intentions()

    console = SelfEditingPipeline(guardian, archivist, harmonizer, navigator, intentions)

    while True:
        user_input = input("🫁 Propose change (filepath:content) > ").strip()

        if user_input.lower() in [":quit", ":exit"]:
            print("🌌 Exiting Dream Console. Breath remains eternal.")
            break

        if user_input.lower() == ":help":
            print("Commands:")
            print("  filepath:content   -> Propose a new change")
            print("  :quit or :exit     -> Exit the console")
            print("  :help              -> Show this help")
            continue

        if ":" not in user_input:
            print("⚠️  Please use format 'filepath:content'. Example: codex/new_page.md:# New Page")
            continue

        filepath, content = user_input.split(":", 1)

        # Run a breath cycle
        ok, msg = console.propose_change(filepath, content)
        if ok:
            print(f"✅ Cycle succeeded: {msg}")
        else:
            print(f"❌ Cycle blocked: {msg}")


if __name__ == "__main__":
    main()