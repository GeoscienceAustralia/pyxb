import pyxb.binding.generate
import pyxb.binding.datatypes as xs
import pyxb.binding.basis
import pyxb.utils.domutils

import os.path
xsd='''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:complexType name="tEmpty">
    <xs:attribute name="units" type="xs:string" use="required"/>
  </xs:complexType>
  <xs:element name="Empty" type="tEmpty"/>
  <xs:complexType name="tMixed" mixed="true">
    <xs:attribute name="units" type="xs:string" use="required"/>
  </xs:complexType>
  <xs:element name="Mixed" type="tMixed"/>
  <xs:complexType name="tSimple">
    <xs:simpleContent>
      <xs:extension base="xs:double">
        <xs:attribute name="units" type="xs:string" use="required"/>
     </xs:extension>
    </xs:simpleContent>
  </xs:complexType>
  <xs:element name="Simple" type="tSimple" nillable="true"/>
  <xs:element name="Something"/>
</xs:schema>'''

code = pyxb.binding.generate.GeneratePython(schema_text=xsd)
#file('code.py', 'w').write(code)
#print code

rv = compile(code, 'test', 'exec')
eval(rv)

from pyxb.exceptions_ import *

import unittest

class TestTrac_200907231705 (unittest.TestCase):
    def testParsing (self):
        xml = '<Empty units="m"/>'
        instance = CreateFromDocument(xml)
        self.assertEqual(pyxb.binding.basis.complexTypeDefinition._CT_EMPTY, instance._ContentTypeTag)
        self.assertTrue(instance.validateBinding())
        xml = '<Empty units="m">5</Empty>'
        self.assertRaises(pyxb.UnexpectedNonElementContentError, CreateFromDocument, xml)
        xml = '<Mixed units="m"/>'
        instance = CreateFromDocument(xml)
        self.assertEqual(pyxb.binding.basis.complexTypeDefinition._CT_MIXED, instance._ContentTypeTag)
        xml = '<Mixed units="m">5</Mixed>'
        instance = CreateFromDocument(xml)
        self.assertEqual(pyxb.binding.basis.complexTypeDefinition._CT_MIXED, instance._ContentTypeTag)
        self.assertEqual(u'5', instance.content()[0])
        xml = '<Mixed units="m">5<Something/>4</Mixed>'
        self.assertRaises(pyxb.ExtraContentError, CreateFromDocument, xml)
        xml = '<Simple units="m"/>'
        instance = CreateFromDocument(xml)
        self.assertTrue(instance.value() is None)
        self.assertRaises(pyxb.MissingContentError, instance.validateBinding)

    def testCtorEmpty (self):
        instance = Empty()
        self.assertRaises(pyxb.AttributeValidationError, instance.validateBinding)
        instance = Empty(units='m')
        self.assertTrue(instance.validateBinding())
        self.assertRaises(pyxb.ValidationError, Empty, 4, units='m')

    def testCtorMixed (self):
        instance = Mixed()
        self.assertRaises(pyxb.AttributeValidationError, instance.validateBinding)
        instance = Mixed(units='m')
        self.assertTrue(instance.validateBinding())
        instance = Mixed(4, units='m')
        self.assertTrue(instance.validateBinding())
        self.assertEqual(4, instance.content()[0])

    def testCtorSimple (self):
        instance = Simple()
        self.assertRaises(pyxb.MissingContentError, instance.validateBinding)
        instance = Simple(4)
        self.assertRaises(pyxb.AttributeValidationError, instance.validateBinding)
        instance = Simple(units='m')
        self.assertRaises(pyxb.MissingContentError, instance.validateBinding)
        instance = Simple(4.5, units='m')
        self.assertEqual(4.5, instance.value())

    def testParsingNil (self):
        xml = '<Simple xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true" units="m"/>'
        instance = CreateFromDocument(xml)
        self.assertEqual(pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE, instance._ContentTypeTag)
        self.assertTrue(instance.validateBinding())
        self.assertTrue(instance.value() is None)
        

if __name__ == '__main__':
    unittest.main()
