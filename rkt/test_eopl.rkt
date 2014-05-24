#lang racket

(require rackunit)
(require rackunit/text-ui)

(require "eopl.rkt")

(define-test-suite test-eopl
  (test-suite
    "test-every"
    (test-true "empty" (every (lambda (x) #f) '()))
    (test-false "not gt" (every (lambda (x) (> x 1)) '(1 2 -1 3)))
    (test-true "numberp" (every number? (list 1 2 -1 3))))
  (test-suite
    "test-exists"
    (test-false "empty" (exists (lambda (x) 0) '()))
    (test-true "is gt" (exists (lambda (x) (> x 1)) (list 1 2 -1 3))))
  (test-suite
    "test-duple"
    (test-equal? "eq" (duple 2 3.14) '(3.14 3.14)))
  (test-suite
    "test-rev"
    (test-equal? "eq" (reverse '(1 2 3)) '(3 2 1)))
  (test-suite
    "test-invert"
    (test-equal? "eq"
                 (invert '((a 1) (a 2)))
                 '((1 a) (2 a))))
  (test-suite
    "test-concat"
    (let* ((x '(1 2 a))
           (y '(c 3 4 5 b))
           (r (concat x y))
           (e '(1 2 a c 3 4 5 b)))
      (test-equal? "eq" r e)))
  (test-suite
    "test-filter-in"
    (let* ((x '(1 2 (a b c) d 34 3.0))
           (r (filter-in (lambda (x) (or (list? x) (symbol? x))) x))
           (e '((a b c) d)))
      (test-equal? "eq" r e))
    (let* ((x '(1 2 (a b c) d 34 3.0))
           (r (filter-in number? x))
           (e '(1 2 34 3.0)))
      (test-equal? "eq" r e)))
  (test-suite
    "test-len"
    (test-equal? "len empty" (length empty) 0)
    (test-equal? "len non empty" (length '(a b 3 4)) 4))
  (test-suite
    "test-lref"
    (test-equal? "lref0" (list-ref (list 1 2 3 'a) 0) 1)
    (test-equal? "lref end" (list-ref (list 1 2 3 'a) 3) 'a))
  (test-suite
    "test-lset"
    (test-equal? "" (list-set (list 'a 1 '(d e)) 2 '(1 2)) '(a 1 (1 2))))
  (test-suite
    "test-product"
    (let ((xys '((() ())
                 ((1 2) ())
                 ((1) (2))
                 ((1) (2 3))
                 ((1 2) (3 4))))
          (solns (list empty
                       empty
                       '((1 2))
                       '((1 2) (1 3))
                       '((1 3) (1 4) (2 3) (2 4)))))
      (for ([xy xys] [soln solns])
        (match-let ([(list x y) xy])
         (test-equal? "product" soln (product x y))))))
  (test-suite
    "test-down"
    (let ((x '(a 2.24 1 b)))
      (test-equal? "flat" '((a) (2.24) (1) (b)) (down x)))
    (let ((x '((a 2.24) 1 b)))
      (test-equal? "nested" '(((a 2.24)) (1) (b)) (down x))))
  (test-suite
    "test-count-occurrences"
    (test-equal? "nested" 4 (count-occurrences 'd '(a (1 2) d ((d) d ((((d)))))))))
  (test-suite
    "test-merge"
    (test-equal? "eq len" (merge '(1 3 5) '(2 4 6)) '(1 2 3 4 5 6))
    (test-equal? "r larg" (merge '(1 3 5) '(3 4 6 8)) '(1 3 3 4 5 6 8))
    (test-equal? "l larg" (merge '(1 3 5 9 11) '(3 4 6 8)) '(1 3 3 4 5 6 8 9 11)))
  (test-suite
    "test-up"
    (test-equal? "singly nested" (up '((1 2) (3 4))) (list 1 2 3 4))
    (let ((x '(a (1 2) d ((d) d ((((d))))))))
      (test-equal? "rat's nest" (up (down x)) x))
    (let ((x '((x (y)) z)))
      (test-equal? "mouse nest" (up x) '(x (y) z))))
  (test-suite
    "test-swapper"
    (test-equal? "basic" '(d b c a) (swapper 'a 'd '(a b c d)))
    (test-equal? "nested"
                 (swapper 'x 'y '((x) y (z (x))))
                 '((y) x (z (y)))))
  (test-suite
    "test-path"
    (let* ((x '(14 (7 () (12 () ()))
                (26 (20 (17 () ()) ()) (31 () ()))))
           (r (path 17 x))
           (e '(right left left)))
      (test-equal? "bst" r e)))
  (test-suite
    "test-my-sort-and-sort-p"
    (let* ((x (shuffle (range 10)))
           (r (my-sort x))
           (t (sort x <))
           (gt (sort x >)))
      (test-equal? "my-sort" r t)
      (test-equal? "gt" (sortp > x) gt)))
  (test-suite
    "test-car-cdr"
    (test-equal? "simple" car (car-cdr 'a '(a b c) 'fail))
    (let* ((lst '(cat lion (fish dog ()) pig))
           (s 'dog)
           (r (car-cdr s lst 'fail))
           (e (compose car (compose cdr (compose car (compose cdr cdr))))))
      (test-equal? "nested" (e lst) (r lst)))))

(run-tests test-eopl)
