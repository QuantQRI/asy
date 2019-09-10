import time

'''单线程IO
def task1():
	print('开始运行task1...')
	time.sleep(2)
	print('task1任务完成，耗时2s')
def task2():
	print('开始运行task2...')
	time.sleep(2)
	print('task2任务完成，耗时2s')
start = time.time()
task1()
task2()
print('所有任务完成，总耗时%.5f秒' % float(time.time()-start))
'''

'''yield和yield from的区别
def generator_1(titles):
	yield titles
def generator_2(titles):
	yield from titles

titles = ['Python', 'Java', 'C++']
for title in generator_1(titles):
	print('生成器1：', title)
结果：
生成器1： ['Python', 'Java', 'C++']
for title in generator_2(titles):
	print('生成器2：', title)
结果：
生成器2：Python
生成器2：Java
生成器2：C++
'''

# yield from自带处理异常
# def generator_1():
# 	total = 0
# 	while True:
# 		x = yield 
# 		print('加',x)
# 		if not x:
# 			break
# 		total += x
# 	return total
# def generator_2(): # 委托生成器
# 	while True:
# 		total = yield from generator_1() # 子生成器
# 		print('加和总数是:',total)
# def main(): # 调用方
# 	# g1 = generator_1()
# 	# g1.send(None)
# 	# g1.send(2)
# 	# g1.send(3)
# 	# g1.send(None)
# 	'''结果
# 	加 3
# 	加 None
# 	  File "F:/py学习/asy/asyp3.py", line 62, in <module>
# 	    main()
# 	  File "F:/py学习/asy/asyp3.py", line 55, in main
# 	    g1.send(None)
# 	StopIteration: 5
# 	'''

# 	g2 = generator_2()
# 	g2.send(None)
# 	g2.send(2)
# 	g2.send(3)
# 	g2.send(None)
# 	'''结果
# 	加 2
# 	加 3
# 	加 None
# 	加和总数是: 5
# 	'''
# main()

# 使用同步方式编写异步功能
# import time
# import asyncio

# @asyncio.coroutine # 标志协程的装饰器
# def taskIO_1():
# 	print('开始运行IO任务1...')
# 	yield from asyncio.sleep(2)  # 假设该任务耗时2s
# 	print('IO任务1已完成，耗时2s')
# 	return taskIO_1.__name__

# @asyncio.coroutine # 标志协程的装饰器
# def taskIO_2():
# 	print('开始运行IO任务2...')
# 	yield from asyncio.sleep(3)  # 假设该任务耗时3s 生成器函数asyncio.sleep()
# 	print('IO任务2已完成，耗时3s')
# 	return taskIO_2.__name__

# @asyncio.coroutine # 标志协程的装饰器
# def main(): # 调用方法
# 	tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
# 	done,pending = yield from asyncio.wait(tasks) # 子生成器
# 	for r in done: # done和pending都是一个任务，所以返回结果需要逐个调用result()
# 		print('协程无序返回值：'+r.result())

# if __name__ == '__main__':
# 	start = time.time()
# 	loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
# 	try:
# 		loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
# 	finally:
# 		loop.close() # 结束事件循环
# 	print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
# # 通过使用协程，极大增加了多任务执行效率，最后消耗的时间是任务队列中耗时最多的时间。上述例子中的总耗时3秒就是taskIO_2()的耗时时间。
# '''
# 开始运行IO任务2...
# 开始运行IO任务1...
# IO任务1已完成，耗时2s
# IO任务2已完成，耗时3s
# 协程无序返回值：taskIO_2
# 协程无序返回值：taskIO_1
# 所有IO任务总耗时3.00390秒
# '''
# import time
# import asyncio
# async def taskIO_1():
# 	print('开始运行IO任务1...')
# 	await asyncio.sleep(2)  # 假设该任务耗时2s
# 	print('IO任务1已完成，耗时2s')
# 	return taskIO_1.__name__
# async def taskIO_2():
# 	print('开始运行IO任务2...')
# 	await asyncio.sleep(3)  # 假设该任务耗时3s
# 	print('IO任务2已完成，耗时3s')
# 	return taskIO_2.__name__

# async def main(): # 调用方
# 	tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
# 	done,pending = await asyncio.wait(tasks) # 子生成器

# 	# done和pending都是一个任务，所以返回结果需要逐个调用result()
# 	此处并发运行传入的aws(awaitable objects)，同时通过await返回一个包含(done, pending)的元组，done表示已完成的任务列表，pending表示未完成的任务列表。
#	注：
#	①只有当给wait()传入timeout参数时才有可能产生pending列表。
#	②通过wait()返回的结果集是按照事件循环中的任务完成顺序排列的，所以其往往和原始任务顺序不同。
# 	for r in done:
# 		print('协程无序返回值：'+r.result())

# if __name__ == '__main__':
# 	start = time.time()
# 	loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
# 	try:
# 		loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
# 	finally:
# 		loop.close() # 结束事件循环
# 	print('所有IO任务总耗时%.5f秒' % float(time.time()-start))

from tqdm import tqdm
import time
# 可视化进度条库
text = ""
for char in tqdm(["a", "b", "c", "d"]):
	time.sleep(1)
	text = text + char

# 如果你只关心协程并发运行后的结果集合，可以使用gather()，它不仅通过await返回仅一个结果集，而且这个结果集的结果顺序是传入任务的原始顺序。
import time
import asyncio
async def taskIO_1():
	print('开始运行IO任务1...')
	await asyncio.sleep(3)  # 假设该任务耗时3s
	print('IO任务1已完成，耗时3s')
	return taskIO_1.__name__
async def taskIO_2():
	print('开始运行IO任务2...')
	await asyncio.sleep(2)  # 假设该任务耗时2s
	print('IO任务2已完成，耗时2s')
	return taskIO_2.__name__
async def main(): # 调用方
	resualts = await asyncio.gather(taskIO_1(), taskIO_2()) # 子生成器
	print(resualts)
	# 返回的是原顺序的输出方式

if __name__ == '__main__':
	start = time.time()
	loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
	try:
		loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
	finally:
		loop.close() # 结束事件循环
	print('所有IO任务总耗时%.5f秒' % float(time.time()-start))
# import time
# import asyncio
# async def taskIO_1():
# 	print('开始运行IO任务1...')
# 	await asyncio.sleep(3)  # 假设该任务耗时3s
# 	print('IO任务1已完成，耗时3s')
# 	return taskIO_1.__name__
# async def taskIO_2():
# 	print('开始运行IO任务2...')
# 	await asyncio.sleep(2)  # 假设该任务耗时2s
# 	print('IO任务2已完成，耗时2s')
# 	return taskIO_2.__name__
# async def main(): # 调用方
# 	tasks = [taskIO_1(), taskIO_2()]  # 把所有任务添加到task中
# 	for completed_task in asyncio.as_completed(tasks):
# 		# 任务执行完毕就率先返回该任务结果
# 		resualt = await completed_task # 子生成器
# 		print('协程无序返回值：'+resualt)

# if __name__ == '__main__':
# 	start = time.time()
# 	loop = asyncio.get_event_loop() # 创建一个事件循环对象loop
# 	try:
# 		loop.run_until_complete(main()) # 完成事件循环，直到最后一个任务结束
# 	finally:
# 		loop.close() # 结束事件循环
# 	print('所有IO任务总耗时%.5f秒' % float(time.time()-start))

# 运行结果
# 开始运行IO任务2...
# 开始运行IO任务1...
# IO任务2已完成，耗时2s
# 协程无序返回值：taskIO_2
# IO任务1已完成，耗时3s
# 协程无序返回值：taskIO_1
# 所有IO任务总耗时3.00300秒
'''
从上面的程序可以看出，使用as_completed(tasks)和wait(tasks)相同之处是返回结果的顺序是协程的完成顺序，
这与gather()恰好相反。而不同之处是as_completed(tasks)可以实时返回当前完成的结果，
而wait(tasks)需要等待所有协程结束后返回的done去获得结果。
'''