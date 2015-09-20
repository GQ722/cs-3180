; Kevin Porter
; "Small Project 1" CS-3180

#lang racket
(require srfi/13)

(define words_list (file->list "linuxwords.txt"))
(define words_string (file->string "linuxwords.txt"))

; Shamelessly stolen from StackOverflow. Turns my list values into proper strings.
; Note: I have a feeling this is kludgy and that I'm just not understanding something.
(define (->string x)
  (call-with-output-string
   (lambda (out)
     (display x out))))

(define count-chars
  (compose length regexp-match*))

(printf "Part 1: List of six letter words in linuxwords that don't contain a e i o.\n\n")

(for-each (lambda (arg)
            (define current (->string arg))
            ; These are the conditions under which we can print words.
            (define (test str) (> (string-length (->string arg)) 5)
              (and (not (string-contains current "A"))
              (and (not (string-contains current "a"))
              (and (not (string-contains current "E"))
              (and (not (string-contains current "e"))
              (and (not (string-contains current "I"))
              (and (not (string-contains current "i"))
              (and (not (string-contains current "O"))
              (and (not (string-contains current "o")))))))))))
            (when (test arg)
              (printf "~a, " arg)
            ))
            words_list)

(define u (count-chars "u" words_string))
(define U (count-chars "U" words_string))

(define total (+ u U))

(printf "\n\nPart 2: number of letter u in linuxwords: ~a" total)
