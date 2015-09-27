#lang racket

(random-seed (current-seconds))
(define num_of_vowels(+ 7 (random 6)))
(define vowels_list '("A" "E" "I" "O" "U"))
(define vowels (list->set vowels_list))

(define uppercase_letters_list (build-list 26 (lambda (x) (make-string 1 (integer->char (+ x (char->integer #\A)))))))
(define uppercase_letters (list->set uppercase_letters_list))

(define consonants (set-subtract uppercase_letters vowels))
(define consonants_list (set->list consonants))

(define num_of_consonants(- 25 num_of_vowels))
(define letters '())
(for ([i num_of_vowels])
  (set! letters (append letters (list (list-ref vowels_list (random 5)))))
)

(for ([i num_of_consonants])
  (set! letters (append letters (list (list-ref consonants_list (random 20)))))
)
(set! letters (shuffle letters))

(define (print_board line)
                    (printf "|---|---|---|---|---|\n|")
                    (for-each (lambda (arg)
                                (printf " ~a |" arg))
                              line)
                    (printf "\n")
  )

(for ([i 5])
  (let () (define idx_start (* i 5))
   (define line '())
   (for ([j 5])
     (set! line (append line (list (list-ref letters (+ idx_start j)))))
     )
   (print_board line)
   )
  )
(printf "|---|---|---|---|---|\n")

(printf "Enter as many words as possible, separated by spaces: ")
(define input (read-line))
