def valid_sid(sid):
    if not (len(sid) == 10): return ["len err"], True
    if not (int(sid[0:2]) in range(48, 67)): return ["2 digit err"], True
    if not (int(sid[2:3]) in [3, 4, 7]): return ["pos 3 not valid"], True
    if not (int(sid[-2:]) in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 51, 53]): return ["last 2 not valid"], True
    return ["Sid is valid"], False