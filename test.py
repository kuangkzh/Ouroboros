import random
import operator


def test():
    print("hello")


func = operator.methodcaller("test")
func()
