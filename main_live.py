
"""
📄 Bestand: main_live.py
🔍 Aangepast: Keep Alive mechanisme toegevoegd om Render wakker te houden.
"""

from aion_core.utils.keep_alive import start_keep_alive

def main():
    # [Hier komt jouw normale setup]
    print("Starting main_live...")

    start_keep_alive()  # ✅ Houd de server wakker

    # [Hier begint jouw eigenlijke tradingloop of processen]
    while True:
        pass  # Placeholder

if __name__ == "__main__":
    main()
