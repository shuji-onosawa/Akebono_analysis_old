#remot path = 'http://darts.isas.jaxa.jp/stp/data/exosd/orbit/daily/'
path = './orbit/19890301.orb'

with open(path) as f:
    for s_line in f:
        print(s_line)