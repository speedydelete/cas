
"""Internal module defining finite sets"""

from __future__ import annotations

from abc import ABC, abstractmethod
import itertools


class FSet:

    """finite (mathematical) set class"""

    def __init__(self, *args: FSet | list | tuple | set | frozenset | int) -> None:
        s = set()
        for arg in args:
            if isinstance(arg, (list, tuple, set, frozenset)):
                arg = FSet(*arg)
            elif arg == 0:
                arg = FSet()
            elif isinstance(arg, int):
                raise ValueError(f'invalid argument for FSet: \'{arg!r}\'')
            else:
                raise TypeError(f'invalid argument for FSet: \'{arg!r}\'')
            s.add(arg)
        self.s = frozenset(s)

    def __repr__(self) -> str:
        return 'FSet(' + ', '.join([repr(x) for x in self.s]) + ')'

    def __str__(self) -> str:
        return 'FSet(' + ', '.join([str(x) for x in self.s]) + ')'

    def __hash__(self) -> int:
        return hash(self.s)

    def __contains__(self, other: FSet) -> bool:
        return other in self.s

    def __le__(self, other: FSet) -> bool:
        return self.s <= other.s

    def __lt__(self, other: FSet) -> bool:
        return self.s < other.s

    def __ge__(self, other: FSet) -> bool:
        return self.s >= other.s

    def __gt__(self, other: FSet) -> bool:
        return self.s > other.s

    def __add__(self, other: FSet | list | tuple | set | frozenset | int) -> FSet:
        return FSet(*self.s, *FSet(other).s)

    def __or__(self, other: FSet) -> FSet:
        return FSet(*(self.s | other.s))

    def __and__(self, other: FSet) -> FSet:
        return FSet(*(self.s & other.s))

    def __sub__(self, other: FSet) -> FSet:
        return FSet(*(self.s - other.s))

    def __xor__(self, other: FSet) -> FSet:
        return FSet(*(self.s ^ other.s))

    def __mul__(self, other: FSet) -> FSet:
        return FSet(*[FSet(*x) for x in itertools.product(self.s, other.s)])

    @property
    def length(self) -> FCardinal:
        '''cardinality'''
        return fset_length(self)

    def power(self):
        '''power set'''
        return FSet(*itertools.chain.from_iterable(itertools.combinations(list(self.s), r) for r in range(len(self.s) + 1)))

    union = __or__
    intersection = intersec = insec = __and__
    difference = diff = __sub__
    symmetric_difference = sym_difference = symmetric_diff = sym_diff = __xor__


class FFSet(FSet, ABC):

    '''fake finite set'''

    def __repr__(self) -> str:
        return object.__repr__(self)
    def __str__(self) -> str:
        return object.__str__(self)
    def __hash__(self) -> int:
        return object.__hash__(self)
    def __contains__(self, other) -> bool:
        return NotImplemented
    def __le__(self, other) -> bool:
        return NotImplemented
    def __lt__(self, other) -> bool:
        return NotImplemented

    @property
    @abstractmethod
    def set(self):
        '''Returns the set representation of an object'''


class FCardinal(FFSet):

    '''Finite cardinal'''

    def __init__(self, value = 0):
        if isinstance(value, FCardinal):
            self.value = value.value
        self.value = int(value)

    def __repr__(self) -> str:
        return f'FCardinal({self.value!r})'

    def __str__(self) -> str:
        return str(self.value)

    def __lt__(self, other: FCardinal):
        return self.value < other.value

    def __le__(self, other: FCardinal):
        return self.value <= other.value

    def __eq__(self, other: FCardinal):
        return self.value == other.value

    def __ne__(self, other: FCardinal):
        return self.value != other.value

    def __gt__(self, other: FCardinal):
        return self.value > other.value

    def __ge__(self, other: FCardinal):
        return self.value >= other.value

    def __hash__(self) -> int:
        return hash(repr(self))

    def __bool__(self) -> bool:
        return bool(self.value)

    def __add__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value + other.value)

    def __sub__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value - other.value)

    def __mul__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value * other.value)

    def __truediv__(self, other: FCardinal) -> FCardinal:
        return FCardinal(round(self.value / other.value))

    def __floordiv__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value // other.value)

    def __mod__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value % other.value)

    def __divmod__(self, other: FCardinal) -> tuple[FCardinal, FCardinal]:
        return (FCardinal(self.value // self.value), FCardinal(self.value % other.value))

    def __pow__(self, other: FCardinal, mod: FCardinal | None = None) -> FCardinal:
        if mod is None:
            return FCardinal(self.value ** other.value)
        return FCardinal(pow(self.value, other.value, mod.value))

    def __lshift__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value << other.value)

    def __rshift__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value >> other.value)

    def __and__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value & other.value)

    def __xor__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value ^ other.value)

    def __or__(self, other: FCardinal) -> FCardinal:
        return FCardinal(self.value | other.value)

    def __neg__(self) -> FCardinal:
        return FCardinal(-self.value)

    def __pos__(self) -> FCardinal:
        return FCardinal(+self.value)

    def __abs__(self) -> FCardinal:
        return FCardinal(abs(self.value))

    def __invert__(self) -> FCardinal:
        return FCardinal(~self.value)

    def __complex__(self) -> complex:
        return complex(self.value)

    def __int__(self) -> int:
        return int(self.value)

    def __float__(self) -> float:
        return float(self.value)

    def __index__(self) -> int:
        return int(self.value)

    def __round__(self, ndigits: int = 0) -> FCardinal:
        return FCardinal(round(self.value, ndigits))

    def __floor__(self) -> FCardinal:
        return FCardinal(self.value.__floor__())

    def __ceil__(self) -> FCardinal:
        return FCardinal(self.value.__ceil__())

    def __trunc__(self) -> FCardinal:
        return FCardinal(self.value.__trunc__())

    @property
    def set(self) -> FSet:
        if self.value == 0:
            return FSet()
        if self.value == 1:
            return FSet(FSet())
        s = (self - FCardinal(1)).set
        return s + s


def fset_length(self: FSet) -> FCardinal:
    '''Internal function'''
    return FCardinal(len(self.s))
