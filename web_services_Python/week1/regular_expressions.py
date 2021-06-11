def calculate(data, findall):
    pattern = r"([abc]{1})([+-]?)=([abc]?)([-+]?\d*)"
    match = findall(pattern)
    for v1, s, v2, n in match:
        if s == '':
            data[v1] = data.get(v2, 0) + int(n or 0)
        elif s == '+':
            data[v1] += data.get(v2, 0) + int(n or 0)
        else:
            data[v1] -= data.get(v2, 0) + int(n or 0)
    return data
