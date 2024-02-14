# autofunc

Provides the @auto wrapper, which allows calling functions with the syntax e.g. `(foo)(1)(2)(c=3)` instead of `foo(1, 2, c=3)`. Also recurses, so `(foo)(foo)(1)(2)(3)(foo)(4)(5)(6)(7)` is viable.

# tests

Tests are in `test.py`, written in `unittest`.