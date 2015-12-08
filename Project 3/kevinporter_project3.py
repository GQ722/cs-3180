"""
Kevin Porter
Project 2
CS-3180

To run the interpreter, simply type 'python kevinporter_project2.py' followed by
the name of the file you want to run. (e.g.,
'python kevinporter_project2.py test2.yolo').
"""

import ast
import itertools
import re
import sys
import random

def find_in(d, k):
    if k in d:
        yield d[k]
    for k in d:
        if isinstance(d[k], list):
            for i in d[k]:
                for j in find_in(i, k):
                    yield j

class Program(object):

    def __init__(self):
        self.classy = False
        self.file = []
        self.line_ptr = 0
        self.looping = False
        self.variables = {}

    def error(self, s):
        print('ERROR: ' + s + ' [Line ' + str(self.line_ptr + 1) + ']'),
        return


    def addition(self, scanner, token):
        values = token.split('+')
        values = [i.replace(' ', '') for i in values]
        for k, value in enumerate(values):
            try:
                values[k] = int(value)
            except:
                try:
                    is_literal = re.match(r'(\'(.*)\')', value)
                    groups = filter(None, is_literal.groups())
                    if len(groups) > 0:
                        values[k] = str(value)
                except:
                    try:
                        values[k] = self.variables[value]
                    except:
                        self.error('Bad addition.')
        value = values[0] + values[1]
        return value


    def end_obj(self, scanner, token):
        self.classy = False


    def obj(self, scanner, token):
        def obj_variable(scanner, token):
            token = token.split()
            try:
                self.variables[name]['variables'][token[1]] = token[-1]
            except:
                d = {
                     'variables': {
                        token[1]: token[-1]
                     }
                }
                self.variables[name] = d

        def obj_function(scanner, token):
            token = token.split()
            try:
                self.variables[name]['functions'][token[-1]] = self.line_ptr
            except:
                d = {
                     'functions': {
                                    token[-1]: self.line_ptr
                     }
                }
                self.variables[name] = d
            self.line_ptr = self.line_ptr + 1
            begin_at = self.line_ptr
            nastiness = list(enumerate(self.file))
            for line_ptr, line in itertools.islice(nastiness, begin_at, len(nastiness)):
                if self.classy:
                    self.line_ptr = line_ptr
                    r = re.match(end_function, line)
                    if r:
                        break
        end_obj = r'(\s*\b(ratchet)\b)'
        value = r'\s*(\'{0,1}[^\[].*\'{0,1}[^\[])'
        variable_declarator = r'(\s*\bswag\b)'
        variable = r'\s*\b[_A-Za-z]+[_A-Za-z0-9]*\b'
        assignment_operator = r'\s*='
        variable_cu = (variable_declarator + r'*' + variable + assignment_operator + value)
        function = r'(fun) ' + variable
        end_function = r'(nuf)'
        values = token.split()
        name = values[1]
        superclass = values[:-1] if 'be' in values else None
        if superclass:
            # the class must implemement a superclass that already exists
            superclass_items = find_in(self.variables, superclass)
            if not superclass_items:
                self.error('Superclass does not exist.')
                return
            else:
                variables = superclass_items['variables']
                functions = superclass_items['functions']
                self.variables[name] = {
                                        'variables': variables,
                                        'functions': functions
                }
        self.classy = True
        self.line_ptr = self.line_ptr + 1
        begin_at = self.line_ptr
        nastiness = list(enumerate(self.file))
        for line_ptr, line in itertools.islice(nastiness, begin_at, len(nastiness)):
            if self.classy:
                self.line_ptr = line_ptr
                s = re.Scanner([
                    (variable_cu, obj_variable),
                    (function, obj_function),
                    (end_obj, self.end_obj),
                ])
                s.scan(line)
            else:
                break


    def comment(self, scanner, token):
        return


    def create_update_variable(self, scanner, token):
        assignment = token.split()
        if 'swag' in assignment: assignment.remove('swag')
        name = assignment.pop(0)
        assignment.pop(0)
        value = ' '.join(assignment)
        is_list = re.match(r'((\s*\[(\s*(((.*))|([0-9]*)),\s*)*\]))', value)
        try:
            groups = filter(None, is_list.groups())
            if len(groups) > 0:
                try:
                    items = value
                    variables = items.replace('[', '')
                    variables = variables.replace(']', '')
                    variables = variables.replace(',', '')
                    variables = re.findall(r'(?<![\S"])([^\'\s]+)(?![\S"])', variables)
                    for i in variables:
                        items = items.replace(i + ',', '')
                    items = ast.literal_eval(items)
                    for i in variables:
                        try:
                            items.append(self.variables[i])
                        except:
                            self.error('Bad reference.')
                    value = items
                except:
                    self.error('Incorrectly formatted list.')
                    return
        except:
            is_literal = re.match(r'^\s*((\'(.*)\')|([0-9]*))\s*$', value)
            if is_literal is not None:
                groups = filter(None, is_literal.groups())
            else:
                try:
                    value = self.parse(value)[0][0]
                except:
                    self.error('Function not found.')
                    return
        try:
            self.variables[name] = int(value)
        except:
            self.variables[name] = value


    def end_loop(self, scanner, token):
        self.looping = False


    def loop(self, scanner, token):
        self.looping = True
        instructions = token.split()
        variable = instructions[1]
        try:
            iteritem = self.variables[instructions[3]]
        except:
            try:
                iteritem = int(iteritem)
            except:
                self.error('Bad loop parameters.')
                return
        self.line_ptr = self.line_ptr + 1
        begin_at = self.line_ptr
        nastiness = list(enumerate(self.file))
        if isinstance(iteritem, int):
            for i in range(iteritem):
                self.variables[variable] = i
                for line_ptr, line in itertools.islice(nastiness, begin_at, len(nastiness)):
                    if self.looping:
                        self.line_ptr = line_ptr
                        self.parse(line)
                    else:
                        break
                self.looping = True
        else:
            for i in iteritem:
                self.variables[variable] = i
                for line_ptr, line in itertools.islice(nastiness, begin_at, len(nastiness)):
                    if self.looping:
                        self.line_ptr = line_ptr
                        self.parse(line)
                    else:
                        break
                self.looping = True


    def multiplication(self, scanner, token):
        values = token.split('*')
        values = [i.replace(' ', '') for i in values]
        for k, value in enumerate(values):
            try:
                values[k] = int(value)
            except:
                try:
                    is_literal = re.match(r'(\'(.*)\')', value)
                    groups = filter(None, is_literal.groups())
                    if len(groups) > 0:
                        values[k] = str(value)
                except:
                    try:
                        values[k] = int(self.variables[value])
                    except:
                        self.error('Bad multiplication.')
        value = values[0] * values[1]
        return value


    def print_command(self, scanner, token):
        token = token.split()
        token.pop(0)
        value = ' '.join(token)
        is_literal = re.match(r'(\s*\[(\s*(\b.*\b),\s*)*\])|(\'(.*)\')|([0-9]*)', value)
        groups = filter(None, is_literal.groups())
        if len(groups) > 0:
            out = str(groups[0])
            out = out.replace('\'', '')
            out = out.replace('\\n', '\n')
            print(out),
        else:
            try:
                if '+' in value:
                    values = value.split('+')
                else:
                    values = [value, ]
                for value in values:

                    item = value.split('[')
                    if len(item) > 1:
                        index = item[1].replace(']', '')
                        variable = item[0]
                        try:
                            index = int(index)
                        except:
                            index = int(self.variables[index])
                        out = self.variables[variable][index]
                        out = out.replace('\'', '')
                        sys.stdout.write(out)
                    else:
                        out = str(self.variables[item[0]])
                        out = out.replace('\'', '')
                        sys.stdout.write(out)
            except:
                self.error('Bad reference.')


    def random(self, scanner, token):
        func, args = token.split('(')
        args = args.replace(')', '')
        args = args.replace(' ', '')
        args = args.split(',')
        if len(args) == 2:
            try:
                val = random.randrange(int(args[0]), int(args[1]))
            except:
                self.error('random() expected two integers. Given at least one string.')
        elif len(args) == 1:
            try:
                val = random.randrange(0, int(args[0]))
            except:
                val = random.choice(self.variables[args[0]])
        else:
            self.error('Improper use of random().')
            return
        return val

    def shuffle(self, scanner, token):
        func, args = token.split('(')
        args = args.replace(')', '')
        args = args.replace(' ', '')
        args = args.split(',')
        if len(args) == 2:
            pass
        elif len(args) == 1:
            val = self.variables[args[0]]
            random.shuffle(val)
        else:
            self.error('Improper use of shuffle().')
            return
        return val

    def subtraction(self, scanner, token):
        values = token.split('-')
        values = [i.replace(' ', '') for i in values]
        for k, value in enumerate(values):
            try:
                values[k] = int(value)
            except:
                try:
                    is_literal = re.match(r'(\'(.*)\')', value)
                    groups = filter(None, is_literal.groups())
                    if len(groups) > 0:
                        values[k] = str(value)
                except:
                    try:
                        values[k] = self.variables[value]
                    except:
                        self.error('Bad subtraction.')
        value = values[0] - values[1]
        return value


    def parse(self, line):
        comment = r'#.*'
        variable_declarator = r'(\s*\bswag\b)'
        variable = r'(\s*(\b[_A-Za-z]+[_A-Za-z0-9]*\b))'
        assignment_operator = r'\s*(=)'
        value = r'(\s*(\'{0,1}[^\[](.*)\'{0,1}[^\[]))'
        list_obj = r'(\s*\[(\s*(\b.*\b),\s*)*\])'
        print_command = r'^(\s*\bholla\b)'
        ratchet = r'(\s*\b(ratchet)\b)'
        on_fleek = r'(\s*\b(on_fleek)\b)'
        random_r = r'(\s*\b(random)\((([0-9]+\s*(,\s*[0-9]+){0,1})|(' + variable + r'))\))'
        shuffle_r = r'(\s*\b(shuffle)\((([0-9]+\s*(,\s*[0-9]+){0,1})|(' + variable + r'))\))'
        loop = r'(\s*\b(naenae)\b\s+(' + variable + r')\s+(in)(' + variable + r'))'
        end_loop = r'\s*\b(groovy)\b'
        variable_cu = (variable_declarator + r'*' + variable + assignment_operator + r'|'.join([value, ]))
        addition = r'(' + r'|'.join([variable, value]) + r')\s*\+\s*(' + '|'.join([variable, value]) + r')'
        subtraction = r'(' + r'|'.join([variable, value]) + r')\s*\-\s*(' + '|'.join([variable, value]) + r')'
        multiplication = r'(' + r'|'.join([variable, value]) + r')\s*\*\s*(' + '|'.join([variable, value]) + r')'
        obj = r'(class) (\w+)( (be a) (\w+))?'
        scanner = re.Scanner([
                              (comment, self.comment),
                              (variable_cu, self.create_update_variable),
                              (variable_declarator + r'*' + variable + assignment_operator + list_obj, self.create_update_variable),
                              (print_command + '(' + '|'.join([value, variable]) + ')', self.print_command),
                              (print_command + list_obj, self.print_command),
                              (loop, self.loop),
                              (end_loop, self.end_loop),
                              (random_r, self.random),
                              (shuffle_r, self.shuffle),
                              (addition, self.addition),
                              (subtraction, self.subtraction),
                              (multiplication, self.multiplication),
                              (obj, self.obj),
                              (r'\s*', None),
                              (r'\z', None),
        ])

        result = scanner.scan(line)
        return result

    def interpret(self):
        for line_ptr, line in enumerate(self.file):
            if line_ptr > self.line_ptr:
                self.line_ptr = line_ptr
                self.parse(line)
        print self.variables

def main(filename):
    program = Program()
    program.file = list(open(filename, 'r'))
    program.interpret()

main(sys.argv[1])
