from ZODB.POSException import ConflictError

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, getUtilitiesFor

from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.contentprovider.interfaces import UpdateNotCalled

from plone.portlets.interfaces import IPortletRetriever
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletManagerRenderer
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType

from plone.portlets.storage import PortletStorage

from plone.memoize.view import memoize

from utils import hashPortletInfo

import logging
logger = logging.getLogger('portlets')

class PortletManagerRenderer(object):
    """Default renderer for portlet managers.

    When the zope.contentprovider handler for the provider: expression looks up
    a name, context, it will find an adapter factory that in turn finds an 
    instance of this class, by doing an adapter lookup for (context, request,
    view, manager).
    """
    implements(IPortletManagerRenderer)
    adapts(Interface, IBrowserRequest, IBrowserView, IPortletManager)
    
    template = None
    error_message = None

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.manager = manager # part of interface
        self.context = context
        self.request = request
        self.__updated = False
        
    @property
    def visible(self):
        portlets = self.portletsToShow()
        return len(portlets) > 0

    def filter(self, portlets):
        return [p for p in portlets if p['assignment'].available]
        
    def portletsToShow(self):
        return self._lazyLoadPortlets(self.manager)

    def update(self):
        self.__updated = True
        for p in self.portletsToShow():
            p.update()

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled
            
        portlets = self.portletsToShow()
        if self.template:
            return self.template(portlets=portlets)
        else:
            return u'\n'.join([p['renderer'].render() for p in portlets])

    def safe_render(self, portlet_renderer):
        try:
            return portlet_renderer.render()
        except ConflictError:
            raise
        except Exception:
            logger.exception('Error while rendering %r' % (self,))
            return self.error_message()

    # Note: By passing in a parameter that's different for each portlet
    # manager, we avoid the view memoization (which is tied to the request)
    # caching the same portlets for all managers on the page. We cache the
    # portlets using a view memo because it they be looked up multiple times,
    # e.g. first to check if portlets should be displayed and later to 
    # actually render
    
    @memoize
    def _lazyLoadPortlets(self, manager):
        retriever = getMultiAdapter((self.context, manager), IPortletRetriever)
        items = []
        for p in self.filter(retriever.getPortlets()):
            renderer = self._dataToPortlet(p['assignment'].data)
            if renderer.available:
                info = p.copy()
                info['manager'] = self.manager.__name__
                info['renderer'] = renderer
                hashPortletInfo(info)
                items.append(info)
        return items
    
    def _dataToPortlet(self, data):
        """Helper method to get the correct IPortletRenderer for the given
        data object.
        """
        return getMultiAdapter((self.context, self.request, self.__parent__,
                                    self.manager, data,), IPortletRenderer)

class PortletManager(PortletStorage):
    """Default implementation of the portlet manager.

    Provides the functionality that allows the portlet manager to act as an
    adapter factory.
    """

    implements(IPortletManager)

    __name__ = __parent__ = None

    def __call__(self, context, request, view):
        return getMultiAdapter((context, request, view, self), IPortletManagerRenderer)

    def getAddablePortletTypes(self):
        return [p[1] for p in getUtilitiesFor(IPortletType) 
                    if p[1].for_ is None or p[1].for_.providedBy(self)]        
