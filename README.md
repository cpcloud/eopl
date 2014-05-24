This is a repository of the exercises for Essentials of Programming
Languages. Some are done in Python (where possible: it's hard to
inspect code in Python) and all are done in Racket.

All code has basic unit tests testing at least the cases presented in
the book, sometimes more.

To the run the tests in Python you need to install ``nose`` and
simple run ``nosetests`` from directory.

For racket, you'll need to run

```sh
raco setup rackunit
```

then to run the tests do

```sh
racket test_eopl.rkt
```
