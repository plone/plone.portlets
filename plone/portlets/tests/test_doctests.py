# -*- coding: utf-8 -*-

from plone.testing import layered

from plone.portlets.testing import PLONEPORTLETS_ZCML_TESTING

import doctest
import unittest


tests = (
    '../utils.txt',
    '../uisupport.txt',
    '../README.txt',
)


def test_suite():
    return unittest.TestSuite(
        [layered(doctest.DocFileSuite(f, optionflags=doctest.ELLIPSIS | doctest.REPORT_ONLY_FIRST_FAILURE),
         layer=PLONEPORTLETS_ZCML_TESTING)
         for f in tests]
    )
