import math
from decimal import Decimal

from django.db.models.functions import Mod
from django.test import TestCase

from ..models import DecimalModel, FloatModel, IntegerModel


class ModTests(TestCase):

    def test_decimal(self):
        DecimalModel.objects.create(n1=Decimal('-9.9'), n2=Decimal('4.6'))
        obj = DecimalModel.objects.annotate(n_mod=Mod('n1', 'n2')).first()
        self.assertIsInstance(obj.n_mod, float)
        self.assertAlmostEqual(obj.n_mod, math.fmod(obj.n1, obj.n2))

    def test_float(self):
        FloatModel.objects.create(f1=-25, f2=0.33)
        obj = FloatModel.objects.annotate(f_mod=Mod('f1', 'f2')).first()
        self.assertIsInstance(obj.f_mod, float)
        self.assertAlmostEqual(obj.f_mod, math.fmod(obj.f1, obj.f2))

    def test_integer(self):
        IntegerModel.objects.create(small=20, normal=15, big=1)
        obj = IntegerModel.objects.annotate(
            small_mod=Mod('small', 'normal'),
            normal_mod=Mod('normal', 'big'),
            big_mod=Mod('big', 'small'),
        ).first()
        self.assertIsInstance(obj.small_mod, float)
        self.assertIsInstance(obj.normal_mod, float)
        self.assertIsInstance(obj.big_mod, float)
        self.assertEqual(obj.small_mod, math.fmod(obj.small, obj.normal))
        self.assertEqual(obj.normal_mod, math.fmod(obj.normal, obj.big))
        self.assertEqual(obj.big_mod, math.fmod(obj.big, obj.small))
