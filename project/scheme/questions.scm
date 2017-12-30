(define (caar x) (car (car x)))
(define (cadr x) (car (cdr x)))
(define (cdar x) (cdr (car x)))
(define (cddr x) (cdr (cdr x)))

; Some utility functions that you may find useful to implement.
(define (map proc items)
  (if (null? items) '()
    (cons (proc (car items)) (map proc (cdr items)))))


(define (cons-all first rests)
  (if (null? rests) nil 
  (cons (cons first (car rests)) (cons-all first (cdr rests)))
  ))

(define (zip pairs)
  (if (null? pairs) '(()()))
  (append (append (cons (caar pairs) nil) (zip (cdr pairs))) (append (cdar pairs) (zip (cdr pairs))))
)

;; Problem 17
;; Returns a list of two-element lists
(define (enumerate s)
  ; BEGIN PROBLEM 17
  (define (count num s)
    (if (null? s) nil
      (cons (cons num (cons (car s) nil)) (count (+ num 1) (cdr s)))
    )
  )
  (count 0 s)
)

  ; END PROBLEM 17

;; Problem 18
;; List all ways to make change for TOTAL with DENOMS
(define (list-change total denoms)
  ; BEGIN PROBLEM 18
  (if (null? denoms) nil
    (if (< (- total (car denoms)) 0)  (list-change total (cdr denoms))
        (if (= (- total (car denoms)) 0) (append (cons(cons (car denoms) nil) nil) (list-change total (cdr denoms)))
            (append (cons-all (car denoms) (list-change (- total (car denoms)) denoms)) (list-change total (cdr denoms))) 

))))
  ; END PROBLEM 18

;; Problem 19
;; Returns a function that checks if an expression is the special form FORM
(define (check-special form)
  (lambda (expr) (equal? form (car expr))))

(define lambda? (check-special 'lambda))
(define define? (check-special 'define))
(define quoted? (check-special 'quote))
(define let?    (check-special 'let))

;; Converts all let special forms in EXPR into equivalent forms using lambda
(define (let-to-lambda expr)
  (cond ((atom? expr)
         ; BEGIN PROBLEM 19
        expr
         ; END PROBLEM 19
         )
        ((quoted? expr)
         ; BEGIN PROBLEM 19
         expr
         ; END PROBLEM 19
         )
        ((or (lambda? expr)
             (define? expr))
         (let ((form   (car expr))
               (params (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
           (cons form (cons params (map let-to-lambda body)))
           ; END PROBLEM 19
           ))
        ((let? expr)
         (let ((values (cadr expr))
               (body   (cddr expr)))
           ; BEGIN PROBLEM 19
            (define forms (map (lambda (x) (let-to-lambda (cadr x))) values))
            (define params (map (lambda (x) (car x)) values))
            (cons (cons 'lambda (cons params (map let-to-lambda body))) forms)
           ; END PROBLEM 19
           ))
        (else
         ; BEGIN PROBLEM 19
         (map let-to-lambda expr)
         ; END PROBLEM 19
         )))
