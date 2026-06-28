import getpass
import sys
from checker import calculate_strength
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

STRENGTH_COLOR = {
    "WEAK":    RED,
    "MEDIUM":  YELLOW,
    "STRONG":  GREEN,
    "INVALID": RED
}

STRENGTH_BANNER = {
    "WEAK":    "❌  WEAK PASSWORD — Not acceptable",
    "MEDIUM":  "⚠️   MEDIUM PASSWORD — Can be improved",
    "STRONG":  "✅  STRONG PASSWORD — Good to go",
    "INVALID": "🚫  INVALID INPUT"
}
def print_banner():
    print(f"\n{BOLD}{CYAN}")
    print("=" * 55)
    print("   🔐  PASSWORD STRENGTH CHECKER")
    print("   DecodeLabs | Cybersecurity Project 1")
    print("=" * 55)
    print(RESET)
def print_result(result: dict, password: str):
    strength = result["strength"]
    color    = STRENGTH_COLOR.get(strength, RESET)
    banner   = STRENGTH_BANNER.get(strength, "")

    print(f"\n{BOLD}{'—' * 45}{RESET}")
    print(f"  Password   : {'*' * len(password)}")
    print(f"  Length     : {result['details'].get('length', {}).get('length', 0)} characters")
    print(f"  Score      : {result['score']} / 7")
    print(f"\n  {BOLD}{color}{banner}{RESET}")
    print(f"{'—' * 45}")
    v = result["details"].get("variety", {})
    if v:
        print(f"\n  Character Mix:")
        print(f"    Uppercase : {'✓' if v['uppercase'] else '✗'}")
        print(f"    Lowercase : {'✓' if v['lowercase'] else '✗'}")
        print(f"    Numbers   : {'✓' if v['digit'] else '✗'}")
        print(f"    Symbols   : {'✓' if v['symbol'] else '✗'}")
    if result["feedback"]:
        print(f"\n  Suggestions:")
        for tip in result["feedback"]:
            print(f"    → {tip}")

    print(f"\n{'—' * 45}\n")


def run_interactive():
    print_banner()
    print("  Type a password to check its strength.")
    print("  Input is hidden for security.")
    print("  Type 'quit' or press Ctrl+C to exit.\n")

    while True:
        try:
            password = getpass.getpass("  Enter password: ")
            if password.lower() in ("quit", "exit", "q"):
                print(f"\n  {CYAN}Exiting. Stay secure! 🔒{RESET}\n")
                break
            result = calculate_strength(password)
            print_result(result, password)
        except KeyboardInterrupt:
            print(f"\n\n  {CYAN}Interrupted. Stay secure! 🔒{RESET}\n")
            break
        except Exception as e:
            print(f"  {RED}Error: {e}{RESET}")
def run_single(password: str):
    print_banner()
    result = calculate_strength(password)
    print_result(result, password)
    return result["strength"]
if __name__ == "__main__":
    if len(sys.argv) > 1:
        # e.g.: python main.py MyPassword123!
        pw = sys.argv[1]
        run_single(pw)
    else:
        run_interactive()
