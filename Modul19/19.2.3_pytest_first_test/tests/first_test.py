# Задание 19.2.3 - Напишите по одному позитивному тесту для каждого метода калькулятора.

import pytest
from app.calculator import Calculator

class TestCalc:
    def setup(self):
        self.calc = Calculator


    def test_multiply(self):
        """Тест функции умножения"""
        assert self.calc.multiply(self, 2, 2) == 4


    def test_division(self):
        """Тест функции деления"""
        assert self.calc.division(self, 2, 2) == 1

    def test_subtraction(self):
        """Тест функции вычитания"""
        assert self.calc.subtraction(self, 4, 1) == 3

    def test_adding(self):
        """Тест функции сложения"""
        assert self.calc.adding(self, 4, 1) == 5
