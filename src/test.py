#!/usr/bin/env python3
'''
fython – More function Python
Copyright © 2014  Mattias Andrée (maandree@member.fsf.org)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


class function:
    def __init__(self, f, n = None, *args):
        self.f = f
        self.n = n if n is not None else f.__code__.co_argcount
        self.args = args
        class code_:
            def __init__(self, n):
                self.co_argcount = n
        self.__code__ = code_(self.n)
    
    
    def __call__(self, *args):
        args = self.args + args
        if len(args) < self.n:
            return function(self.f, self.n, *args)
        else:
            return self.f(*args)
    
    
    @staticmethod
    def __combine(fg, f, g):
        rc = lambda *args : fg(f(*args), g(*args))
        rc = function(rc, f.__code__.co_argcount)
        return rc
    
    
    def __add__(self, f):
        return function.__combine(lambda x, y : x + y, self.f, f)
    
    def __sub__(self, f):
        return function.__combine(lambda x, y : x - y, self.f, f)
    
    def __mul__(self, f):
        return function.__combine(lambda x, y : x * y, self.f, f)
    
    def __truediv__(self, f):
        return function.__combine(lambda x, y : x / y, self.f, f)
    
    def __mod__(self, f):
        return function.__combine(lambda x, y : x % y, self.f, f)
    
    def __divmod__(self, f):
        return function.__combine(lambda x, y : divmod(x, y), self.f, f)
    
    def __lshift__(self, f):
        return function.__combine(lambda x, y : x << y, self.f, f)
    
    def __rshift__(self, f):
        return function.__combine(lambda x, y : x >> y, self.f, f)
    
    def __pow__(self, f, m = None):
        if m is None:
            return function.__combine(lambda x, y : x ** y, self.f, f)
        else:
            return function.__combine(lambda x, y : pow(x, y, m), self.f, f)
    
    
    def __radd__(self, f):
        return function.__combine(lambda x, y : x + y, f, self.f)
    
    def __rsub__(self, f):
        return function.__combine(lambda x, y : x - y, f, self.f)
    
    def __rmul__(self, f):
        return function.__combine(lambda x, y : x * y, f, self.f)
    
    def __rtruediv__(self, f):
        return function.__combine(lambda x, y : x / y, f, self.f)
    
    def __rmod__(self, f):
        return function.__combine(lambda x, y : x % y, f, self.f)
    
    def __rdivmod__(self, f):
        return function.__combine(lambda x, y : divmod(x, y), f, self.f)
    
    def __rlshift__(self, f):
        return function.__combine(lambda x, y : x << y, f, self.f)
    
    def __rrshift__(self, f):
        return function.__combine(lambda x, y : x >> y, f, self.f)
    
    def __rpow__(self, f, m = None):
        if e is None:
            return function.__combine(lambda x, y : x ** y, f, self.f)
        else:
            return function.__combine(lambda x, y : pow(x, y, m), f, self.f)
    
    
    def __eq__(self, f):
        return function.__combine(lambda x, y : x == y, self.f, f)
    
    def __ge__(self, f):
        return function.__combine(lambda x, y : x >= y, self.f, f)
    
    def __gt__(self, f):
        return function.__combine(lambda x, y : x > y, self.f, f)
    
    def __le__(self, f):
        return function.__combine(lambda x, y : x <= y, self.f, f)
    
    def __lt__(self, f):
        return function.__combine(lambda x, y : x < y, self.f, f)
    
    def __ne__(self, f):
        return function.__combine(lambda x, y : x != y, self.f, f)
    
    
    def __and__(self, f):
        rc = lambda *args : function(self.f)(f(*args))
        rc = function(rc, f.__code__.co_argcount)
        return rc
    
    def __rand__(self, f):
        rc = lambda *args : function(f)(self.f(*args))
        rc = function(rc, self.f.__code__.co_argcount)
        return rc
    
    
    def combine(self, f, op):
        return function.__combine(lambda x, y : op(x, y), self.f, f)


@function
def f1(a, b):
    return a + b

@function
def f2(a, b):
    return a * b

print((f1 & f2)(2, 2)(3))
print(f1.combine(f2, lambda x, y : x ** y)(1, 3))

