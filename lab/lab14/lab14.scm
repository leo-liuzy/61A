(define (foldl fn init lst)
    (if (null? lst)
      init
      (foldl fn (fn init (car lst)) (cdr lst))))

(define (foldr fn init lst)
  (if (null? lst) init
    (fn (car lst) (foldr fn init (cdr lst)))))

(define (map lst fn)
  (foldr (lambda (x xs) (cons (fn x) xs) nil lst)
))

(define (assert-equal value expression)
  (if (equal? value (eval expression))
    (print 'ok)
    (print (list 'for expression ':
                 'expected value
                 'but 'got (eval expression)))))

(define (map fn s)
  (if (null? s) nil
      (cons (fn (car s))
            (map fn (cdr s)))))

(define (filter fn s)
  (cond ((null? s) nil)
        ((fn (car s)) (cons (car s)
                            (filter fn (cdr s))))
        (else (filter fn (cdr s)))))

(define (tally names)
  (map (lambda (name) (cons name (count name names))) (unique names)))



(define (test-tally)
  (print (list 'testing 'tally))
  (assert-equal '((obama . 1))
                '(tally '(obama)))
  (assert-equal '((taft . 3))
                '(tally '(taft taft taft)))
  (assert-equal '((jerry . 2) (brown . 1))
                '(tally '(jerry jerry brown)))
  (assert-equal '((jane . 5) (jack . 2) (jill . 1))
                '(tally '(jane jack jane jane jack jill jane jane)))
  (assert-equal '((jane . 5) (jack . 2) (jill . 1))
                '(tally '(jane jack jane jane jill jane jane jack)))
  )

; Using this helper procedure is optional. You are allowed to delete it.
(define (unique s)
  (if (null? s) nil
      (cons (car s)
            (unique (filter (lambda (x) (not (eq? (car s) x))) (cdr s))))))
; Using this helper procedure is optional. You are allowed to delete it.
(define (count name s)
  (if (null? s) 0
      (+ (if (eq? name (car s)) 1 0)
         (count name (cdr s)))))

; Passing these tests is optional. You are allowed to delete them.
(define (test-tally-helpers)
  (print (list 'testing 'unique))
  (assert-equal '(jane)  '(unique '(jane jane jane)))
  (assert-equal '(jane jack jill)  '(unique '(jane jack jane jack jill jane)))
  (assert-equal '(jane jack jill)  '(unique '(jane jack jane jill jane jack)))
  (print (list 'testing 'count))
  (assert-equal 3 '(count 'jane '(jane jane jane)))
  (assert-equal 0 '(count 'jill '(jane jane jane)))
  (assert-equal 2 '(count 'jack '(jane jack jane jack jill jane)))
  )

;(test-tally-helpers)
;(test-tally)
