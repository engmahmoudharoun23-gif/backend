lines_to_inspect = [2482, 2527, 3490, 3676, 3690, 10102, 10146, 10381, 10529, 10580]
with open('server.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for idx in lines_to_inspect:
        print(f"{idx}: {ascii(lines[idx-1])}")
