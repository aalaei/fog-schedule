import hashlib
import os


def try_num(problem_context, nonce, difficulty_level):
    sliced_none = []
    while nonce > 0:
        sliced_none.append(chr(nonce % 256))
        nonce = int(nonce // 256)
    new_str = problem_context.decode().replace("?", "".join(sliced_none))
    return hashlib.sha256(new_str.encode()).hexdigest()[:difficulty_level] == ('0' * difficulty_level)


def computational_task(name, difficulty_level):
    f = open(name, "rb")
    problem_context = f.read()
    f.close()
    nonce = 1
    while not try_num(problem_context, nonce, difficulty_level):
        nonce += 1
    os.remove(name)
    return nonce