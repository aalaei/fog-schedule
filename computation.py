import hashlib
import os
import sys
from time import time

def try_num(problem_context, nonce, difficulty_level):
    sliced_none = []
    while nonce > 0:
        sliced_none.append(chr(nonce % 256))
        nonce = int(nonce // 256)
    new_str = problem_context.decode().replace("?", "".join(sliced_none))
    bin_hash_code =  hashlib.sha256(new_str.encode()).hexdigest()

    return bin_hash_code[:difficulty_level] == ('0' * difficulty_level)


def computational_task(name, difficulty_level):
    f = open(name, "rb")
    problem_context = f.read()
    f.close()
    nonce = 1
    while not try_num(problem_context, nonce, difficulty_level):
        nonce += 1
    os.remove(name)
    return nonce


if __name__ == '__main__':
    t1=time()
    if len(sys.argv)<2:
        difficulty_level=5
    else:
        difficulty_level = eval(sys.argv[1])
    problem_context ="seggseg?srgsdr".encode()
    nonce = 1
    while not try_num(problem_context, nonce, difficulty_level):
        nonce += 1
    t2=time()
    print("passed time={}".format(t2-t1))