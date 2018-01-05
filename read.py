f = open('./fights_2018-01-04.csv', 'r')

lines = []
for line in f.read().splitlines():
    lines.append(line)

print '# of lines = ', len(lines)
