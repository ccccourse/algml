```

(env) cccimac@cccimacdeiMac nim % python nim1.py -v
Trying:
    print(nim([1, 2, 3], MISERE))
Expecting:
    misere [1, 2, 3] You will lose :(
ok
Trying:
    print(nim([1, 2, 3], NORMAL))
Expecting:
    normal [1, 2, 3] You will lose :(
ok
Trying:
    print(nim([1, 2, 4], MISERE))
Expecting:
    misere [1, 2, 4] (2, 1)
ok
Trying:
    print(nim([1, 2, 4], NORMAL))
Expecting:
    normal [1, 2, 4] (2, 1)
ok
Trying:
    print(nim([1], MISERE))
Expecting:
    misere [1] You will lose :(
ok
Trying:
    print(nim([1], NORMAL))
Expecting:
    normal [1] (0, 1)
ok
Trying:
    print(nim([1, 1], MISERE))
Expecting:
    misere [1, 1] (0, 1)
ok
Trying:
    print(nim([1, 1], NORMAL))
Expecting:
    normal [1, 1] You will lose :(
ok
Trying:
    print(nim([1, 5], MISERE))
Expecting:
    misere [1, 5] (1, 5)
ok
Trying:
    print(nim([1, 5], NORMAL))
Expecting:
    normal [1, 5] (1, 4)
ok
1 item had no tests:
    __main__
1 item passed all tests:
  10 tests in __main__.nim
10 tests in 2 items.
10 passed.
Test passed.

```