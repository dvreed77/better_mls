
def get_key(fname):
    with open(fname, 'r') as f:
        first_line = f.readline()

    return first_line.strip()
