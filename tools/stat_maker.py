"""
This module is used to make new stats that are balanced
"""

RES_EXPECTED = 2.25

while True:
    stats_infos = []

    i = 0
    stop = False
    while not stop:
        input_ = input(f'STAT {i} | <nom> <type> <%importance>: ')

        try:
            input_split = input_.split(' ')
            name = input_split[0]

            type_stat, importance = map(float, input_split[1:])

            stats_infos.append((name, type_stat, importance))
            i += 1
        except ValueError:
            stop = True

    res = []
    for infos in stats_infos:
        type_stat = infos[1]

        if type_stat == 1:
            value = RES_EXPECTED * infos[2] / 100
            res.append(value)
        else:
            value = RES_EXPECTED * infos[2] / 150
            res.append(value)

    for i in range(len(res)):
        print(f'{stats_infos[i][0]}: {res[i]}')

