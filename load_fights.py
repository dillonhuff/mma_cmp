from fight import *
from utils import *

def load_fights(f):
    lines = []
    for line in f.read().splitlines():
        lines.append(line)

    print '# of lines = ', len(lines)

    proc_lines = []

    for line in lines:
        tokens = []

        for tok in line.split(' '):
            for tk in tok.split('\t'):
                tokens.append(tk)

        proc_lines.append(tokens)

    fights = []
    for proc_line in proc_lines:
        f1 = proc_line[0]
        f2 = proc_line[1]
        res = proc_line[2]
        cause = proc_line[3]

        i = 4
        while not is_month(proc_line[i]):
            i += 1

        assert(is_month(proc_line[i]))

        month = proc_line[i]

        assert(proc_line[i + 1] == '/')

        day = proc_line[i + 2]

        assert(proc_line[i + 3] == '/')

        year = proc_line[i + 4]

        if represents_int(year) and represents_int(day):
            dt = Date(month, int(day), int(year))

            fights.append(Fight(f1, f2, res, cause, dt))

    return fights
