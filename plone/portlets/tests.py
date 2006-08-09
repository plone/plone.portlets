import unittest

import zope.app
import zope.app.component
import plone.portlets

from zope.testing import doctest
from zope.app.testing.placelesssetup import setUp, tearDown
from zope.configuration.xmlconfig import XMLConfig

optionflags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS

def configurationSetUp(test):
    setUp()
    XMLConfig('meta.zcml', zope.app.component)()
    XMLConfig('configure.zcml', plone.portlets)()

def configurationTearDown(test):
    tearDown()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt', 
            setUp=configurationSetUp, 
            tearDown=configurationTearDown,
            optionflags=optionflags),
        ))

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')