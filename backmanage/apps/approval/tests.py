from django.test import TestCase

# Create your tests here.

# a = {'name': 'zhang', 'age': 10}

# if not isinstance(eval('[1,2,3]'), list):
#     print('545')
# else:
#     print(type(eval('[1,2,3]')))

#
# print(str(33333).zfill(4))
# print(type(str(3).zfill(4)))
#
# print(10**3)

# print(type(eval('[1,2,3]')))


# import time
#
#
# def deco(func):
#     startTime = time.time()
#     func()
#     endTime = time.time()
#     msecs = (endTime - startTime) * 1000
#     print("time is %d ms" % msecs)
#
#
# def func():
#     print("hello")
#     time.sleep(1)
#     print("world")
#
#
# if __name__ == '__main__':
#     f = func
#     deco(f)
#     print("f.__name__ is", f.__name__)  # f的name就是func()
#     print()


# 既不需要侵入，也不需要函数重复执行
# import time
#
#
# def deco(func):
#     def wrapper():
#         startTime = time.time()
#         func()
#         endTime = time.time()
#         msecs = (endTime - startTime) * 1000
#         print("time is %d ms" % msecs)
#     return wrapper
#
#
# @deco
# def func():
#     print("hello")
#     time.sleep(1)
#     print("world")
#
#
# if __name__ == '__main__':
#     f = func  # 这里f被赋值为func，执行f()就是执行func()
#     f()

# 带有参数的装饰器
# import time
#
#
# def deco(func):
#     def wrapper(a, b):
#         startTime = time.time()
#         func(a, b)
#         endTime = time.time()
#         msecs = (endTime - startTime) * 1000
#         print("time is %d ms" % msecs)
#
#     return wrapper
#
#
# @deco
# def func(a, b):
#     print("hello，here is a func for add :")
#     time.sleep(1)
#     print("result is %d" % (a + b))
#
#
# if __name__ == '__main__':
#     f = func
#     f(3, 4)
# func()


# 带有不定参数的装饰器
# import time
#
# def deco(func):
#     def wrapper(*args, **kwargs):
#         startTime = time.time()
#         func(*args, **kwargs)
#         endTime = time.time()
#         msecs = (endTime - startTime)*1000
#         print("time is %d ms" %msecs)
#     return wrapper
#
#
# @deco
# def func(a,b):
#     print("hello，here is a func for add :")
#     time.sleep(1)
#     print("result is %d" %(a+b))
#
# @deco
# def func2(a,b,c):
#     print("hello，here is a func for add :")
#     time.sleep(1)
#     print("result is %d" %(a+b+c))
#
#
# if __name__ == '__main__':
#     f = func
#     func2(3,4,5)
#     f(3,4)

# 多个装饰器

# import time
#
#
# def deco01(func):
#     def wrapper(*args, **kwargs):
#         print("this is deco01")
#         startTime = time.time()
#         func(*args, **kwargs)
#         endTime = time.time()
#         msecs = (endTime - startTime) * 1000
#         print("time is %d ms" % msecs)
#         print("deco01 end here")
#
#     return wrapper
#
#
# def deco02(func):
#     def wrapper(*args, **kwargs):
#         print("this is deco02")
#         func(*args, **kwargs)
#
#         print("deco02 end here")
#
#     return wrapper
#
#
# @deco01
# @deco02
# def func(a, b):
#     print("hello，here is a func for add :")
#     time.sleep(1)
#     print("result is %d" % (a + b))
#
#
# if __name__ == '__main__':
#     f = func
#     f(3, 4)
#     # func()


# def dec1(func):
#     print("1111")
#     def one():
#         print("2222")
#         func()
#         print("3333")
#     return one
#
# def dec2(func):
#     print("aaaa")
#     def two():
#         print("bbbb")
#         func()
#         print("cccc")
#     return two
#
# @dec1
# @dec2
# def test():
#     print("test test")
#
# test()
