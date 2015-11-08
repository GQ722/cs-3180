;; Kevin Porter
;; Small Project 2

#lang racket

(define (check_comment string)
  (define result (regexp-match (pregexp "^\\/\\/.*$") string))
  result)

(define (check_comment_blank result string)
  (and (not (equal? result '()) )
  (not (check_comment string)))
  )

(define (is_number string)
  (define result (regexp-match* (pregexp "(\\b\\d+\\.\\d*)|(\\b\\d+\\.\\b)|(\\b\\d+\\b)") string))
  (when (check_comment_blank result string) (printf "~a\n" result)))

(define (is_symbol string)
  (define result (regexp-match* (pregexp "\\b[_A-Za-z]+[_A-Za-z0-9]*\\b") string))
  (when (check_comment_blank result string) (printf "~a\n" result)))

(define (is_comment string)
  (define result (regexp-match* (pregexp "^\\/\\/.*$") string))
  (when (check_comment_blank result string) (printf "~a\n" result)))

(define (is_operator string)
  (define result (regexp-match* (pregexp "\\+|-|\\*|\\/") string))
  (when (check_comment_blank result string) (printf "~a\n" result)))

(define (is_parenthesis string)
  (define result (regexp-match* (pregexp "\\(|\\)") string))
  (when (check_comment_blank result string) (printf "~a\n" result)))

;; Racket doesn't like the \z regex operator?
(define (is_EOF string)
  (define result (regexp-match* (pregexp "\\z") string))
  (when (not (equal? result '()) )(printf "~a\n" result)))

(define (error string)
  (when (not (regexp-match-exact? (pregexp "((\\b\\d+\\.\\d*)|(\\b\\d+\\.\\b)|(\\b\\d+\\b)|(\\b[_A-Za-z]+[_A-Za-z0-9]*\\b)|(^\\/\\/.*$)|(\\+|-|\\*|\\/)|(\\(|\\))|\\s)*") string)
    )
    (printf "ERROR\n"))
)


(define (parse string)
  (is_number string)
  (is_symbol string)
  (is_comment string)
  (is_operator string)
  (is_parenthesis string)
  (error string)
  )

(parse "1.0 asdf 2.3423 3 44.")
(parse "asd 234f asdf32 _a23fa23f")
(parse "// some comment")
(parse "+-*/")
(parse "()")
(parse "asdf asdf () 2345asdf")