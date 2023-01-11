import sys
import os


IGNORE = ["git", "__pycache__", ".db", "tools", "swp", "log.dat"]


def find_or_replace(line_no, line, path, term, replacement = None):
    if replacement:
        r = line.replace(term, replacement)
        l = line.rstrip('\n')
        print(f"\n{path}")
        print(f"#{line_no} > {l}")
        print(f"#{line_no} > {r}")
    else:
        print(f" line #{line_no}: {path}")


def prompt():
    choice = input("Do you want to commit these changes [y/N]?\n>>> ")
    choice = True if choice.lower() == "y" else False
    return choice


def search(term, replacement, confirm):
    for root, directories, files in os.walk("."):
        for file in files:
            try:
                path = os.path.join(root, file)
                for flag in IGNORE:
                    assert not flag in path
            except AssertionError:
                continue
            else:
                line_no, found = 1, False
                with open(path, "r") as fhand:
                    try:
                        for line in fhand:
                            if term in line:
                                find_or_replace(line_no, line, path, term, 
                                        replacement)
                                found = True
                            line_no += 1

                        choice = False
                        if replacement and found and confirm:
                            choice = prompt()
                        elif replacement and found:
                            choice = True
                        if choice:
                            fhand.seek(0)
                            text = fhand.read()
                            text = text.replace(term, replacement)
                    except UnicodeDecodeError:
                        continue

                if choice:
                    with open(path, "w") as fhand:
                        fhand.write(text)

if __name__ == "__main__":
    term = sys.argv[1]
    try:
        replacement = sys.argv[2]
    except IndexError: replacement = None

    try:
        confirm = False if sys.argv[3].lower() == "false" else True
    except IndexError: confirm = True
    
    search(term, replacement, confirm)
