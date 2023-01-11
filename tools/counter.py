import os

def count():
    statement_counter = 0
    line_counter      = 0
    for root, directories, files in os.walk("."):
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".sql"):
                path = os.path.join(root, fname)
                print(path)
                with open(path, "r") as fhand:
                    for line in fhand:
                        length = len(line.strip())
                        if length:
                            statement_counter += 1
                        line_counter += 1
    return statement_counter, line_counter


if __name__ == "__main__":
    s, l = count()
    print(f"There are {s} statements out of {l} lines.")
