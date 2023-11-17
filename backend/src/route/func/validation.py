from route.func.errmaker import errmaker
import json


def bvsid(sid, sql):
    if not (len(sid) == 10): return ["len err"], True
    if not (int(sid[0:2]) in range(48, 67)): return ["2 digit err"], True
    if not (int(sid[2:3]) in [3, 4, 7]): return ["pos 3 not valid"], True
    if not (int(sid[-2:]) in [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 51, 53]): return ["last 2 not valid"], True
    return ["Sid is valid"], False

def valid_sid(sid, sql):
    _, err = bvsid(sid)
    if err:
        return errmaker(400, "Sid in invalid"), True
    return "all good", False

def valid_sc(sc, sql):
    result, err = sql.sqsel("users", ["subjects", "sid"], f"secret_code='{sc}'")
    if err:
        return errmaker(400, "secret_code not found"), True
    return result, False

def valid_token(ip, sid, token, task, sql):
    result, err = sql.sqsel("users", ["token"], f"sid='{sid}'")
    if err:
        return result, True

    if len(result) == 0:
        return errmaker(400, "user not found"), True
    
    tokendb = json.loads(result[0][0])

    if token not in tokendb.values():
        result, err = sql.sqadd("logs", ["ip", "info"], [ip, f'trying to {task} sid={sid} data but token is unauthorized'])
        if err:
            return result, True
        return errmaker(400, "token is unauthorized"), True
    
    return "all good", False