#lang eopl


(provide (all-defined-out))


(define (every pred lst)
  (or (null? lst) (and (pred (car lst)) (every pred (cdr lst)))))


(define (exists pred lst)
  (and (not (null? lst)) (or (pred (car lst)) (exists pred (cdr lst)))))


(define (concat lst1 lst2)
  (cond
    [(and (null? lst1) (null? lst2)) empty]
    [(null? lst1) lst2]
    [(null? lst2) lst1]
    [else (cons (car lst1) (concat (cdr lst1) lst2))]))


(define (length x)
  (if (null? x)
    0
    (+ 1 (length (cdr x)))))


(define (take lst n)
  (if (zero? n)
    empty
    (cons (car lst) (take (cdr lst) (- n 1)))))


(define (product los1 los2)
  (if (exists null? (list los1 los2))
    empty
    (cons (list (car los1) (car los2))
        (concat (product (take los1 1) (cdr los2))
                (product (cdr los1) los2)))))


(define (sum x)
  (cond
    [(null? x) 0]
    [else (+ (car x) (sum (cdr x)))]))


(define (prod x)
  (exp (sum (map log x))))


(define (map f lst)
  (cond
    [(null? lst) empty]
    [else (cons (f (car lst)) (map f (cdr lst)))]))


(define (duple n x)
  (cond
    [(zero? n) empty]
    [else (cons x (duple (- n 1) x))]))


(define (reverse lst)
  (cond
    [(null? lst) empty]
    [(concat (reverse (cdr lst)) (take lst 1))]))


(define (fold f initial lst)
  (cond
    [(= 1 (length lst)) (f (car lst) initial)]
    [else
      (f (car lst) (fold f initial (cdr lst)))]))


(define (invert lst)
  (if (null? lst)
    '()
    (concat (list (reverse (car lst))) (invert (cdr lst)))))


(define (filter-in pred lst)
  (if (null? lst)
    '()
    (if (not (pred (car lst)))
      (filter-in pred (cdr lst))
      (cons (car lst) (filter-in pred (cdr lst))))))


(define (list-ref x i)
  (if (zero? i)
    (car x)
    (list-ref (cdr x) (- i 1))))


(define (list-set lst n x)
  (if (zero? n)
    (cons x (cdr lst))
    (cons (car lst) (list-set (cdr lst) (- n 1) x))))


(define (down lst)
  (if (null? (cdr lst))
    (list lst)
    (cons (take lst 1) (down (cdr lst)))))


(define (count-in s lst)
  (if (null? lst)
    0
    (+ (if (equal? (car lst) s) 1 0) (count-in s (cdr lst)))))


(define (flatten lst)
  (if (null? lst)
    empty
    (if (not (list? (car lst)))
      (cons (car lst) (flatten (cdr lst)))
      (concat (flatten (car lst)) (flatten (cdr lst))))))


(define (count-occurrences s lst)
  (count-in s (flatten lst)))


(define (merge lst1 lst2)
  (cond
    [(and (null? lst1) (not (null? lst2))) lst2]
    [(and (null? lst2) (not (null? lst1))) lst1]
    [(every null? (list lst1 lst2)) empty]
    [(<= (car lst1) (car lst2))
     (concat (cons (car lst1) (take lst2 1)) (merge (cdr lst1) (cdr lst2)))]
    [else
      (concat (cons (car lst2) (take lst1 1)) (merge (cdr lst1) (cdr lst2)))]))


(define (up lst)
  (cond
    [(null? lst) empty]
    [(not (list? (car lst))) (cons (car lst) (up (cdr lst)))]
    [else (concat (car lst) (up (cdr lst)))]))


(define (swapper a b lst)
  (cond
    [(null? lst) empty]
    [else
      (let* ((c (car lst))
             (to-cons
               (cond
                 [(eq? c a) b]
                 [(eq? c b) a]
                 [(list? c) (swapper a b c)]
                 [else c])))
        (cons to-cons (swapper a b (cdr lst))))]))


(define (path x bst)
  (cond
    [(null? bst) empty]
    [(eq? (car bst) x) empty]
    [(< (car bst) x) (cons 'right (path x (caddr bst)))]
    [else (cons 'left (path x (cadr bst)))]))


(define (filter pred lst)
  (cond
    [(null? lst) empty]
    [(not (pred (car lst))) (filter pred (cdr lst))]
    [else
      (cons (car lst) (filter pred (cdr lst)))]))


(define (my-sort lst)
  (sortp < lst))


(define (negate f)
  (lambda rst (not (apply f rst))))


(define neq? (negate eq?))
(define notnull? (negate null?))


(define (sortp pred lst)
  (cond
    [(<= (length lst) 1) lst]
    [else
      (let* ((piv (list-ref lst (floor (/ (length lst) 2))))
             (lhs (filter (lambda (x) (pred x piv)) lst))
             (rhs (filter (lambda (x) (and (not (pred x piv)) (neq? x piv)))
                          lst)))
        (concat (sortp pred lhs) (cons piv (sortp pred rhs))))]))


(define (compose f g)
  (lambda (x) (f (g x))))


(define (car-cdr s lst errvalue)
  (cond
    [(null? lst) (lambda (x) errvalue)]
    [(eq? (car lst) s) car]
    [(list? (car lst)) (compose (car-cdr s (car lst) errvalue) car)]
    [else
      (compose (car-cdr s (cdr lst) errvalue) cdr)]))


(define (occurs-free? var expr)
  (cond
    [(symbol? expr) (eqv? var expr)]
    [(eqv? (car expr) 'lambda)
          (and (neq? (caadr expr) var)
               (occurs-free? var (caddr expr)))]
    [else
      (or (occurs-free? var (cadr expr))
          (occurs-free? var (car expr)))]))
