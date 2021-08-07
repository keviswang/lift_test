'''
假设你正在开发电梯的控制调度系统，请设计这个调度系统的控制逻辑，并能够响应以下场景：

1. 客人在第n层按向上、向下的按钮
2. 客人等待电梯到达
3. 系统调度某个电梯去接应客人
4. 客人进入电梯的时候能够指定目标楼层
5. 在到达目标楼层途中可以响应其他同向的客人
6. ...

注：请关注调度逻辑，忽略非调度相关的细节（如超重等），其他合理的场景不一一举例，思考的全面程度也是考核点之一

【任务1】：请用伪代码设计，只需要写interface并辅助文字说明即可，如下：

```python
class controller(object):
	def func_A(x, y, z):
		'''函数目的 + 参数解释, 不需要写具体实现代码'''

	def func_B(x, y, z):
		'''函数目的 + 参数解释, 不需要写具体实现代码'''

'''
调用流程解释：
当（1）客人在第n层按按钮时，触发`func_A`；
然后控制器然后去做xxx事情，调用`func_B`做yyy事情。

'''
```

【任务2】：如果想提高电梯单位时间载人量（效率），请论述有什么可以提高的方法？
'''

