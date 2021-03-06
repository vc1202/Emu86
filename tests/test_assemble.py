#!/usr/bin/env python3
"""
Test our assembly interpreter.
"""

import sys
import random
sys.path.append("..")

import operator as opfunc

from unittest import TestCase, main

from assembler.global_data import gdata
from assembler.assemble import assemble

NUM_TESTS = 100
BIG_NEG = -10000
BIG_POS = 10000

class AssembleTestCase(TestCase):

    def test_mov(self):
        assemble("mov eax, 1", gdata)
        self.assertEqual(gdata.registers["EAX"], 1)

    def two_op_test(self, operator, instr):
        for i in range(0, NUM_TESTS):
            a = random.randint(BIG_NEG, BIG_POS)
            b = random.randint(BIG_NEG, BIG_POS)
            correct = operator(a, b)
            gdata.registers["EAX"] = a
            gdata.registers["EBX"] = b
            assemble(instr + " eax, ebx", gdata)
            self.assertEqual(gdata.registers["EAX"], correct)

    def test_add(self):
        self.two_op_test(opfunc.add, "add")

    def test_sub(self):
        self.two_op_test(opfunc.sub, "sub")

    def test_imul(self):
        self.two_op_test(opfunc.mul, "imul")

    def test_and(self):
        self.two_op_test(opfunc.and_, "and")

    def test_or(self):
        self.two_op_test(opfunc.or_, "or")

    def test_xor(self):
        self.two_op_test(opfunc.xor, "xor")

    def test_shl(self):
        gdata.registers["EAX"] = 18                      
        assemble("shl eax, 2", gdata)
        self.assertEqual(gdata.registers["EAX"], 72)     

    def test_shr(self):
        gdata.registers["EAX"] = 18                      
        assemble("shr eax, 2", gdata)
        self.assertEqual(gdata.registers["EAX"], 4)      

    def test_neg(self):
        gdata.registers["EAX"] = 18
        assemble("neg eax", gdata)
        self.assertEqual(gdata.registers["EAX"], -18)

    def test_not(self):
        gdata.registers["EAX"] = 18
        assemble("not eax", gdata)
        self.assertEqual(gdata.registers["EAX"], -19)
 
    def test_inc(self):
        gdata.registers["EAX"] = 18
        assemble("inc eax", gdata)
        self.assertEqual(gdata.registers["EAX"], 19)

    def test_dec(self):
        gdata.registers["EAX"] = 18
        assemble("dec eax", gdata)
        self.assertEqual(gdata.registers["EAX"], 17)

    def test_idiv(self):
        gdata.registers["EAX"] = 1
        gdata.registers["EDX"] = 1
        gdata.registers["EBX"] = 2
        assemble("idiv ebx", gdata)
        self.assertEqual(gdata.registers["EAX"], 2147483648)
        self.assertEqual(gdata.registers["EDX"], 1)

    def test_cmp_eq(self):
        gdata.registers["EAX"] = 1
        gdata.registers["EBX"] = 1
        gdata.flags["ZF"] = 0
        gdata.flags["SF"] = 0
        assemble("cmp eax, ebx", gdata)
        self.assertEqual(gdata.flags["ZF"], 1)
        self.assertEqual(gdata.flags["SF"], 0)

    def test_cmp_l(self):
        gdata.registers["EAX"] = 0
        gdata.registers["EBX"] = 1
        gdata.flags["ZF"] = 0
        gdata.flags["SF"] = 0
        assemble("cmp eax, ebx", gdata)
        self.assertEqual(gdata.flags["ZF"], 0)
        self.assertEqual(gdata.flags["SF"], 1)
        
if __name__ == '__main__':
    main()
