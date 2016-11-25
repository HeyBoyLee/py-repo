# encoding: utf-8
# 装饰器 跟返回的函数无关
import functools


def log(func):
    @functools.wraps(func)
    def xxx(*args, **kw):
        print 'call %s' % func.__name__
        return func(*args, **kw)
    return xxx


# decorator本身需要传入参数 (两层嵌套)
# 以上两种decorator的定义都没有问题，但还差最后一步。因为我们讲了函数也是对象，它有__name__等属性，但你去看经过decorator装饰之后的函数，它们的__name__已经从原来的'now'变成了'wrapper'：
# functools.wraps(func) 可以解决上述问题
def log1(text):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            print '%s %s():' % (text, func.__name__)
            return func(*args, **kw)
        return wrapper
    return decorator
