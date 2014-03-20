#!/usr/bin/env python3
'''
fython – More functional Python
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
        self.overloads = []
        self.chain = []
    
    
    def __call__(self, *args):
        args = self.args + args
        if len(args) < self.n:
            f = function(self.f, self.n, *args)
            f.overloads = self.overloads[:]
            f.chain = self.chain[:]
            return f
        else:
            def test(value, reqs, guards, i):
                if ((reqs is None) or (reqs[i] is None)):
                    if ((guards is None) or (guards[i] is None)):
                        return True
                    return guards[i](value)
                req_ = True
                if isinstance(reqs[i], type):
                    req_ = isinstance(value, reqs[i])
                else:
                    req_ = value == reqs[i]
                if not req_:
                    return False
                if ((guards is None) or (guards[i] is None)):
                    return True
                return guards[i](value)
            rc = None
            for f, ts, gs in self.overloads:
                if all([test(args[i], ts, gs, i) for i in range(self.n)]):
                    rc = f(*args)
                    break
            else:
                rc = self.f(*args)
            if len(self.chain) == 0:
                return rc
            return tuple([rc] + [f(*args) for f in self.chain])
    
    
    def overload(self, *types):
        if not len(types) == self.n: # TODO make this unnecessary
            raise Exception('Incompatible number of arguments')
        class overload_:
            def __init__(self, that):
                self.that = that
            def __call__(self, f):
                self.that.overloads.append((f, types, None))
                return self.that
            def guard(self, *testers): # TODO see guard outside overload
                if not len(testers) == self.that.n:
                    raise Exception('Incompatible number of arguments')
                def guard_(f):
                    self.that.overloads.append((f, types, testers))
                    return self.that
                return guard_
        return overload_(self)
    
    
    def guard(self, *testers):
        # TODO make this unnecessary
        # TODO allow multiparameter testers, for example
        #      lambda a, b : a == 0 and b == 1
        #      instead of
        #      lambda a : a == 0, lambda b : b == 1
        if not len(testers) == self.n:
            raise Exception('Incompatible number of arguments')
        def guard_(f):
            self.overloads.append((f, None, testers))
            return self
        return guard_
    
    
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
    
    
    def __or__(self, f):
        rc = function(self.f, self.n, *(self.args))
        rc.overloads = self.overloads[:]
        rc.chain = self.chain[:]
        rc.chain.append(f)
        return rc
    
    # TODO add __ror__
    
    
    def combine(self, f, op):
        return function.__combine(lambda x, y : op(x, y), self.f, f)


F = function


f1 = F(lambda a, b : a + b)
f2 = F(lambda a, b : a * b)

print((f1 & f2)(2, 2)(3))
print(f1.combine(f2, lambda x, y : x ** y)(1, 3))

@F
def f(a):
    return 'default:%s' % repr(a)

o = f.overload(int)
@o.guard(lambda x : x == 0)
# TODO it should be possible to add more guards here,
# that extend this guard with additional arguments,
# not alternative conditions
def f(_a):
    return 'zero'

@f.overload(1)
def f(_a):
    return 'one'

@f.guard(lambda x : x == 2)
def f(_a):
    return 'two'

@f.overload(int)
def f(a):
    return 'int:%i' % a

@f.overload(str)
def f(a):
    return 'str:%s' % a

print(f(0))
print(f(1))
print(f(2))
print(f(3))
print(f('1'))
print(f({}))

@F
def f1(a):
    return a ** 2

@F
def f2(a):
    return a ** 3

@F
def f3(a):
    return a ** 4

print((f1 | f2 | f3)(2))


