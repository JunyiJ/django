import math
from decimal import Decimal

from django.db.models import DecimalField
from django.db.models.functions import Ln
from django.test import TestCase

from ..models import DecimalModel, FloatModel, IntegerModel


class LnTests(TestCase):

    def test_decimal(self):
        DecimalModel.objects.create(n1=Decimal('12.9'), n2=Decimal('0.6'))
        obj = DecimalModel.objects.annotate(n1_ln=Ln('n1'), n2_ln=Ln('n2')).first()
        self.assertAlmostEqual(obj.n1_ln, math.log(obj.n1))
        self.assertAlmostEqual(obj.n2_ln, math.log(obj.n2))

    def test_float(self):
        FloatModel.objects.create(f1=27.5, f2=0.33)
        obj = FloatModel.objects.annotate(f1_ln=Ln('f1'), f2_ln=Ln('f2')).first()
        self.assertAlmostEqual(obj.f1_ln, math.log(obj.f1))
        self.assertAlmostEqual(obj.f2_ln, math.log(obj.f2))

    def test_integer(self):
        IntegerModel.objects.create(small=20, normal=15, big=1)
        obj = IntegerModel.objects.annotate(
            small_ln=Ln('small'),
            normal_ln=Ln('normal'),
            big_ln=Ln('big'),
        ).first()
        self.assertAlmostEqual(obj.small_ln, math.log(obj.small))
        self.assertAlmostEqual(obj.normal_ln, math.log(obj.normal))
        self.assertAlmostEqual(obj.big_ln, math.log(obj.big))

    def test_transform(self):
        try:
            DecimalField.register_lookup(Ln)
            DecimalModel.objects.create(n1=Decimal('12.0'), n2=Decimal('0'))
            DecimalModel.objects.create(n1=Decimal('1.0'), n2=Decimal('0'))
            objs = DecimalModel.objects.filter(n1__ln__gt=0)
            self.assertQuerysetEqual(objs, [12.0], lambda a: a.n1)
        finally:
            DecimalField._unregister_lookup(Ln)
