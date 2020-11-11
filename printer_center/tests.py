from django.test import TestCase

# Create your tests here.


a = 0


def fun():
    global a  # 声明全局变量a
    print(a)
    b = a + 1
    a = b
    print(b)

def fun2():
    print(a+4)

fun()
fun2()

