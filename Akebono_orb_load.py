date = '19890301'
file_name = date + '.orb'
folder_path = './orbit/'

path = folder_path + file_name

with open(path, mode = 'r') as f:
    print(type(f))
    lines = f.readlines()
    print(len(lines))