"""
Kevin Porter
Small Project 2
CS-3180
"""
import re

def operator(scanner, token): return token
def number(scanner, token): return token
def comment(scanner, token): return token
def symbol(scanner, token): return token
def parenthesis(scanner, token): return token
def EOF(scanner, token): return token

def scan(s):
    """
    I took some liberty and allowed whitespaces.
    """

    scanner = re.Scanner([
                            (r'\b[_A-Za-z]+[_A-Za-z0-9]*\b', symbol),
                            (r'^\/\/.*$', comment),
                            (r'\b\d+\.\d*', number),
                            (r'\b\d+\.\b', number),
                            (r'\b\d+\b', number),
                            (r'\+|-|\*|\/', operator),
                            (r'\(|\)', parenthesis),
                            (r'\s*', None),
                            (r'\z', EOF),
    ])
    result = scanner.scan(s)
    if len(result) > 0:
        print result[0]
        if len(result[1]) > 0:
            print('ERROR')
    else:
        print(result)

def test():
    parenthesis = '( )'
    symbols = '_Abcd123 ABCD123'
    not_symbols = '123abcd -abdc3'
    comment = '// this is a comment'
    numbers = '1 123 1.23 1. 1.2'
    operators = '+-*/'
    EOF = ''

    scan(parenthesis)
    scan(symbols)
    scan(not_symbols)
    scan(comment)
    scan(numbers)
    scan(operators)
    scan(EOF)

test()
