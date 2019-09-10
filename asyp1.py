import asyncio
import time
'''
#列表生成式
lis = [x*x for x in range(10)]
print(lis)
'''
#生成器
generator_ex = (x*x for x in range(10))
print(generator_ex)
# 可以逐个打印，当到最后时报StopIteration错误
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
print(next(generator_ex))
# 为了不报错的使用迭代器，使用for循环是常用做法
for i in generator_ex:
	print(i)
# 斐波那契数列-普通函数形式
#fibonacci数列
def fib(max):
	n,a,b =0,0,1
	while n < max:
		# a,b = b ,a+b  其实相当于 t =a+b ,a =b ,b =t  ，所以不必写显示写出临时变量t
		a,b =b,a+b
		n = n+1
		print(a)
	return 'done'

a = fib(10)
print(fib(10))

# 斐波那契数列-生成器形式
def fib(max):
	n,a,b =0,0,1
	while n < max:
		yield b
		a,b =b,a+b
		n = n+1
	return 'done'
# fib()函数为生成器形式
a = fib(10)
print(fib(10))
print(a.__next__())
print(a.__next__())
print(a.__next__())
print("可以顺便干其他事情")
print(a.__next__())
print(a.__next__())
# 生成器next()调用时候从上次的返回yield语句处执行，内存需要多少用多少
# 生成器最大的好处就是，循环不再占据全部内存，再循环的时候可以做其他事情

# 自定义迭代器，同样用for循环来迭代
for i in fib(6):
	print(i)
# 但是用for循环得不到生成器最后的返回值，因此要捕捉StopIteration错误，返回值包含在StopIteration的value中
g = fib(6)
while True:
	try:
		x = next(g)
		print('generator: ',x)
	except StopIteration as e:
		print("生成器返回值：",e.value)
		break

# 函数有了yield之后，函数名+()就变成了生成器
# return在生成器中代表生成器的中止，直接报错
# next的作用是唤醒并继续执行
# send的作用是唤醒并继续执行，发送一个信息到生成器内部
# send()和next()的区别就在于send可传递参数给yield表达式，这时候传递的参数就会作为yield表达式的值，而yield的参数是返回给调用者的值，也就是说send可以强行修改上一个yield表达式值。
def consumer(name):
	print("%s 准备学习啦!" %name)
	while True:
		lesson = yield
		print("开始[%s]了,[%s]老师来讲课了!" %(lesson,name))

def producer(name):
	c = consumer('A')
	c2 = consumer('B')
	c.__next__()
	c2.__next__()
	print("同学们开始上课 了!")
	for i in range(10):
		time.sleep(1)
		print("到了两个同学!")
		c.send(i)
		c2.send(i)
'''
运行结果：
A 准备学习啦!
B 准备学习啦!
同学们开始上课 了!
到了两个同学!
开始[0]了,[A]老师来讲课了!
开始[0]了,[B]老师来讲课了!...
'''
def create_counter(n):
	print("create_counter")
	while True:
		yield n
		print("increment n")
		n +=1

gen = create_counter(2)
print(gen)
print(next(gen))
print(next(gen))
'''
结果：
<generator object create_counter at 0x0000023A1694A938>
create_counter
2
increment n
3
Process finished with exit code 0
'''
# 可迭代的Iterable 生成器都是Iterator对象，但list、dict、str虽然是Iterable（可迭代对象），却不是Iterator（迭代器）
# 迭代器（迭代就是循环）可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。
num = [0,1,2,3,4]
# 把list、dict、str等Iterable变成Iterator可以使用iter()函数
t = iter(num)
for i in t:
	print(next(t))
# def get_num():
# 	print(t.__next__())
# 	get_num()
s='hello'     #字符串是可迭代对象，但不是迭代器
l=[1,2,3,4]     #列表是可迭代对象，但不是迭代器
t=(1,2,3)       #元组是可迭代对象，但不是迭代器
d={'a':1}        #字典是可迭代对象，但不是迭代器
set={1,2,3}     #集合是可迭代对象，但不是迭代器

f=open('test.txt') #文件是可迭代对象，是迭代器
# 及可迭代对象通过__iter__转成迭代器对象
from collections import Iterator  #迭代器
from collections import Iterable  #可迭代对象

print(isinstance(s,Iterator))     #判断是不是迭代器
print(isinstance(s,Iterable))       #判断是不是可迭代对象

#把可迭代对象转换为迭代器
print(isinstance(iter(s),Iterator))

'''小节
1.凡是可作用于for循环的对象都是Iterable类型；
2.凡是可作用于next()函数的对象都是Iterator类型，它们表示一个惰性计算的序列；
3.集合数据类型如list、dict、str等是Iterable但不是Iterator，不过可以通过iter()函数获得一个Iterator对象。
'''
def d():
	print('初始化')
	sum = 0
	value = yield sum
	sum = sum + value
	print('sum的值是：%d' % sum)
	value = yield sum
	sum = sum + value
	print('sum的值是：%d' % sum)
	value = yield sum
	sum = sum + value
	print('sum的值是：%d' % sum)
	return sum + 1
c = d()
a = c.send(None)
# print('生成器传出的值为：%d' % a)
# a = c.send(1)
# print('生成器传出的值为：%d' % a)
# a = c.send(1)
# print('生成器传出的值为：%d' % a)
while True:
	print('生成器传出的值为：%d' % a)
	try:
		a = c.send(1)
	except StopIteration as e:
		print('生成器最后传出的值为：%d' % e.value)
		break

# 生成器表达式
[x*x for x in range(10)]# 列表生成器表达式
(x*x for x in range(10))# 元组生成器表达式