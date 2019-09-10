# 函数装饰器
# @+函数将@后的语句结果作为前一句函数的参数
def funA(fn):
	print('A')
	fn() # 执行传入的fn参数
	return 'fkit'
'''
下面装饰效果相当于：funA(funB)，
funB将会替换（装饰）成该语句的返回值；
由于funA()函数返回fkit，因此funB就是fkit
'''
@funA
def funB():
	print('B')
print(funB) # fkit
'''
# 将 funB 作为 funA() 的参数，也就是上面代码中 @funA 相当于执行 funA(funB)。
# 将 funB 替换成上一步执行的结果，funA() 执行完成后返回 fkit，因此 funB 就不再是函数，而是被替换成一个字符串。
被修饰的函数总是被替换成 ＠ 符号所引用的函数的返回值，因此被修饰的函数会变成什么，完全由于 ＠ 符号所引用的函数的返回值决定，换句话说，如果 ＠ 符号所引用的函数的返回值是函数，那么被修饰的函数在替换之后还是函数。
'''
# 装饰器的复杂运用
def foo(fn):
	# 定义一个嵌套函数
	def bar(*args):
		print("===1===", args)
		n = args[0]
		print("===2===", n * (n - 1))
		# 查看传给foo函数的fn函数
		print(fn.__name__)
		fn(n * (n - 1))
		print("*" * 15)
		return fn(n * (n - 1))
	return bar
'''
下面装饰效果相当于：foo(my_test)，
my_test将会替换（装饰）成该语句的返回值；
由于foo()函数返回bar函数，因此funB就是bar
'''
@foo
def my_test(a):
	print("==my_test函数==", a)
# 打印my_test函数，将看到实际上是bar函数
print(my_test) # <function foo.<locals>.bar at 0x00000000021FABF8>
# 下面代码看上去是调用my_test()，其实是调用bar()函数
my_test(10)
my_test(6, 5)
'''
上面程序定义了一个装饰器函数 foo，该函数执行完成后并不是返回普通值，而是返回 bar 函数（这是关键），这意味着被该 ＠foo 修饰的函数最终都会被替换成 bar 函数。
上面程序使用 ＠foo 修饰 my_test() 函数，因此程序同样会执行 foo(my_test)，并将 my_test 替换成 foo() 函数的返回值：bar 函数。
所以，上面程序第二行粗体字代码在打印 my_test 函数时，实际上输出的是 bar 函数，这说明 my_test 已经被替换成 bar 函数。接下来程序两次调用 my_test() 函数，实际上就是调用 bar() 函数。
'''