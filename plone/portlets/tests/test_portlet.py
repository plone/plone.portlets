# -*- coding: utf-8 -*-

from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletRetriever
from plone.portlets.manager import PortletManagerRenderer
from plone.portlets.retriever import PortletRetriever
from plone.portlets.testing import PLONEPORTLETS_INTEGRATION_TESTING

from zope.annotation.attribute import AttributeAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import adapts
from zope.component import provideAdapter
from zope.interface import classImplements
from zope.interface import implements
from zope.interface import Interface
from zope.publisher.browser import TestRequest

import unittest2 as unittest


class TestPortlet(unittest.TestCase):

    layer = PLONEPORTLETS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_safe_render(self):

        # Render the portlet safely, so that when an exception
        # occurs, we log and don't bail out.

        class PortletRenderer:
            def __init__(self, error=False):
                self.error = error

            def render(self):
                if self.error:
                    raise Exception()
                return 'portlet rendered'

        # When no error occurs, ``safe_render`` will return the portlet
        # renderer's ``render()``:

        renderer = PortletManagerRenderer(*(None,) * 4)
        self.assertEquals(renderer.safe_render(PortletRenderer()), 'portlet rendered')

        # When an error is raised, the ``error_message`` template is
        # rendered:

        renderer.error_message = lambda: 'error rendered'
        self.assertEquals(renderer.safe_render(PortletRenderer(error=True)), 'error rendered')

    def test_portlet_metadata_availability(self):

        # Check that the __portlet_metadata__ field is available when
        # the PortletManagerRenderer checks for the availability of
        # the PortletRenderers

        # Define a dummy PortletManager
        class IDummyPortletManager(IPortletManager):
            "Dummy portlet manager"

        class DummyPortletManager:
            implements(IDummyPortletManager)
            __name__ = None

        # Define a dummy PortletRenderer that is only available in case
        # it has __portlet_metadata__

        class DummyPortletRenderer:
            implements(IPortletRenderer)

            @property
            def available(self):
                return getattr(self, '__portlet_metadata__', False)

            def render(self):
                return u'dummy portlet renderer'

            def update(self):
                pass

        # Define a dummy portlet retriever that adapts our dummy portlet manager
        # and returns in its getPortlets a mock dictinary with a dummy
        # PortletRenderer as p['assignment'].data. For that, we need a class
        # where we can set an attribute 'data'

        class Obj(object):
            pass

        class DummyPortletRetriever(PortletRetriever):
            implements(IPortletRetriever)
            adapts(Interface, IDummyPortletManager)

            def getPortlets(self):
                p = dict()
                p['category'] = CONTEXT_CATEGORY
                p['key'] = p['name'] = u'dummy'
                p['assignment'] = obj = Obj()
                obj.data = DummyPortletRenderer()
                obj.available = True
                return (p, )

        provideAdapter(DummyPortletRetriever)

        classImplements(TestRequest, IAttributeAnnotatable)
        provideAdapter(AttributeAnnotations)

        # We need a dummy context that implements Interface

        class DummyContext(object):
            implements(Interface)

        # We now test the PortletManagerRenderer. We override the _dataToPortlet
        # method since our data is already our correct (dummy) IPortletRenderer

        def _dataToPortlet(self, data):
            return data
        PortletManagerRenderer._dataToPortlet = _dataToPortlet

        # Check that a PortletManagerRenderer is capable of rendering our
        # dummy PortletRenderer

        renderer = PortletManagerRenderer(DummyContext(),
                                          TestRequest(),
                                          None, DummyPortletManager())
        renderer.update()
        self.assertEquals(renderer.render(), u'dummy portlet renderer')
