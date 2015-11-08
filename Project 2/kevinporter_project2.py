"""
Kevin Porter
Project 2
CS-3180
"""

import ast
import itertools
import re
import sys


class Program(object):

    def __init__(self):
        self.file = []
        self.line_ptr = 0
        self.looping = False
        self.variables = {}

    def error(self, s):
        print('ERROR: ' + s + ' [Line ' + str(self.line_ptr + 1) + ']')
        return


    def comment(self, scanner, token):
        return


    def create_update_variable(self, scanner, token):
        assignment = token.split()
        if 'swag' in assignment: assignment.remove('swag')
        name = assignment.pop(0)
        assignment.pop(0)
        value = ' '.join(assignment)
        is_list = re.match(r'(\s*\[(\s*(\b.*\b),\s*)*\])', value)
        try:
            groups = filter(None, is_list.groups())
            if len(groups) > 0:
                try:
                    value = ast.literal_eval(value)
                except:
                    self.error('Incorrectly formatted list.')
                    return
        except:
            pass
        self.variables[name] = value


    def end_loop(self, scanner, token):
        self.looping = False


    def loop(self, scanner, token):
        self.looping = True
        instructions = token.split()
        variable = instructions[1]
        iteritem = self.variables[instructions[3]]
        self.line_ptr = self.line_ptr + 1
        begin_at = self.line_ptr
        nastiness = list(enumerate(self.file))
        for i in iteritem:
            self.variables[variable] = i
            for line_ptr, line in itertools.islice(nastiness, begin_at, len(nastiness)):
                if self.looping:
                    self.line_ptr = line_ptr
                    self.parse(line)
                else:
                    break
            self.looping = True



    def print_command(self, scanner, token):
        token = token.split()
        token.pop(0)
        value = ' '.join(token)
        is_literal = re.match(r'(\s*\[(\s*(\b.*\b),\s*)*\])|(\'(.*)\')|([0-9])*', value)
        groups = filter(None, is_literal.groups())
        if len(groups) > 0:
            print(groups[0])
        else:
            try:
                print(self.variables[value])
            except:
                self.error('Bad reference')


    def parse(self, line):
        comment = r'#.*'
        variable_declarator = r'(\s*\bswag\b)'
        variable = r'(\s*(\b[_A-Za-z]+[_A-Za-z0-9]*\b))'
        assignment_operator = r'\s*(=)'
        value = r'(\s*(\'*[^\[](\w+)\'*[^\[]))'
        list_obj = r'(\s*\[(\s*(\b.*\b),\s*)*\])'
        print_command = r'^(\s*\bholla\b)'
        ratchet = r'(\s*\b(ratchet)\b)'
        on_fleek = r'(\s*\b(on_fleek)\b)'
        loop = r'(\s*\b(naenae)\b\s+(' + variable + r')\s+(in)(' + variable + r'))'
        end_loop = r'\s*\b(groovy)\b'
        variable_cu = (variable_declarator + r'*' + variable + assignment_operator + r'|'.join([value, ]))
        scanner = re.Scanner([
                              (comment, self.comment),
                              (variable_cu, self.create_update_variable),
                              (variable_declarator + r'*' + variable + assignment_operator + list_obj, self.create_update_variable),
                              (print_command + '(' + '|'.join([value, variable]) + ')', self.print_command),
                              (print_command + list_obj, self.print_command),
                              (loop, self.loop),
                              (end_loop, self.end_loop),
                              (r'\s*', None),
                              (r'\z', None),
        ])

        result = scanner.scan(line)

    def interpret(self):
        for line_ptr, line in enumerate(self.file):
            if line_ptr > self.line_ptr:
                self.line_ptr = line_ptr
                self.parse(line)

def main(filename):
    program = Program()
    program.file = list(open(filename, 'r'))
    program.interpret()

main(sys.argv[1])
