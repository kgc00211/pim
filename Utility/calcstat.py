# coding: utf-8

"""docs."""

import argparse as argp
import statistics
import sys
from math import cos, sin, tan, sqrt


def argparse_argp(argvs=None):
    """args."""
    parser = argp.ArgumentParser()
    subparsers = parser.add_subparsers(help='c:計算  s:統計  r:逆ポーランド')

    # create the parser for the "cal" command
    parser_c = subparsers.add_parser('c', help='算術式計算', prefix_chars=':')
    parser_c.add_argument('mode', action='store_const',
                          const='calc', default='calc')
    parser_c.add_argument('calc', nargs='*', help='計算式')

    # create the parser for the "sta" command
    parser_s = subparsers.add_parser('s', help='統計量計算')
    parser_s.add_argument('mode', action='store_const',
                          const='stat', default='stat')
    parser_s.add_argument('nums', nargs='+', help='数値１，数値２，…')
    parser_s.add_argument('-fmt', nargs=1,
                          default='%8.3f', help='出力フォーマット')

    # create the parser for the "rpn" command
    parser_r = subparsers.add_parser('r', help='ＲＰＮ計算')
    parser_r.add_argument('mode', action='store_const',
                          const='rpnc', default='rpnc')
    parser_r.add_argument('rpnc', nargs='*', help='逆ポーランド記法')

    args = parser.parse_args() if argvs is None else parser.parse_args(argvs)
    return args


class rpncalc(object):
    """class rpn."""

    # from collections import deque
    ops = ['+', '-', '*', '/', 'c', '@']    # c:change_sign  p:y**x  @:x⇔y
    sep = ops + [' ', '\t', ',']

    def __init__(self, formula=None):
        """init."""
        from collections import deque
        self.dd = deque([0])
        self.xyzt = [0]
        if formula is None:
            self.formula = ''
        else:
            self.formula_token(formula)

    def formula_token(self, formula):
        """test."""
        self.formula = formula
        ss = ''
        for s in self.formula:
            if s in self.__class__.sep:
                if ss != '':
                    self.dd.append(float(ss))
                if s in self.__class__.ops:
                    self.dd.append(s)
                ss = ''
            else:
                ss += s
        if ss != '':
            self.dd.append(float(ss))

    def calculation(self):
        """calc."""
        for i in range(len(self.dd)):
            d = self.dd.popleft()
            if d in self.__class__.sep:
                x = self.xyzt.pop()
                y = self.xyzt.pop()
                if d == '+':
                    self.xyzt.append(y + x)
                if d == '-':
                    self.xyzt.append(y - x)
                if d == '*':
                    self.xyzt.append(y * x)
                if d == '/':
                    self.xyzt.append(y / x)
            elif d == 'c':
                self.xyzt[-1] = - self.xyzt[-1]
            else:
                self.xyzt.append(d)
        return self.xyzt[-1]


def rpn(arg=''):
    """rpn do."""
    if len(arg) > 0:
        rpnc = ' '.join(arg)
        rpn = rpncalc(rpnc)
        r = rpn.calculation()
        print('rpnc = %s = %s' % (rpnc, r))
    else:
        rpn = rpncalc()
        while 1:
            rpnc = input('rpnc = ')
            if rpnc == '':
                break
            rpn.formula_token(rpnc)
            r = rpn.calculation()
            print('rpnc = %s = %s' % (rpnc, r))
    return None


def calc_do(arg=''):
    """calc_do."""
    if len(arg) > 0:
        coms = ''.join(arg)
        print('coms = %s = %s' % (coms, eval(coms)))
    else:
        while 1:
            coms = input('coms = ')
            if coms == '':
                break
            print('coms = %s = %s' % (coms, eval(coms)))
    return None

if __name__ == '__main__':

    p = sys.argv[1:] if len(sys.argv) > 1 else ['-h']
    args = argparse_argp(p)
    # print(args)

    print()
    if args.mode == 'calc':
        calc_do(args.calc)
        print()
    elif args.mode == 'stat':
        print('num  = %s' % len(args.nums))
        print('min  = %s' % min(args.nums))
        print('max  = %s' % max(args.nums))
        if len(args.nums) > 1:
            nums = [float(x) for x in args.nums]
            fmt = ''.join(args.fmt)
            print ('sum  = %s' % sum(nums))
            print(('mean = ' + fmt) % statistics.mean(nums))
            print(('stdv = ' + fmt) % statistics.stdev(nums))
            print(('vari = ' + fmt) % statistics.variance(nums))
    elif args.mode == 'rpnc':
        rpn(args.rpnc)
        print()
