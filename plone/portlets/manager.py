from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, getUtilitiesFor

from zope.publisher.interfaces.http import IHTTPRequest
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IBrowserRequest

from zope.contentprovider.interfaces import UpdateNotCalled

from plone.portlets.interfaces import IPortletRetriever
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletManagerRenderer
from plone.portlets.interfaces import IPortletRenderer
from plone.portlets.interfaces import IPortletType

from plone.portlets.storage import PortletStorage

class PortletManagerRenderer(object):
    """Default renderer for portlet managers.

    When the zope.contentprovider handler for the provider: expression looks up
    a name, context, it will find an adapter factory that in turn finds an 
    instance of this class, by doing an adapter lookup for (context, request,
    view, manager).
    """
    implements(IPortletManagerRenderer)
    adapts(Interface, IBrowserRequest, IBrowserView, IPortletManager)

    def __init__(self, context, request, view, manager):
        self.__parent__ = view
        self.manager = manager # part of interface
        self.context = context
        self.request = request
        self.template = None
        self.__updated = False
        self.__portlets = None
        
    @property
    def visible(self):
        portlets = self._lazyLoadPortlets()
        return len(portlets) > 0

    def filter(self, portlets):
        return [p for p in portlets if p.available]

    def update(self):
        self.__updated = True
        for p in self._lazyLoadPortlets():
            p.update()

    def render(self):
        if not self.__updated:
            raise UpdateNotCalled()
            
        portlets = self._lazyLoadPortlets()
        if self.template:
            return self.template(portlets=portlets)
        else:
            return u'\n'.join([p.render() for p in portlets])

    def _lazyLoadPortlets(self):
        if self.__portlets is None:
            retriever = getMultiAdapter((self.context, self.manager), IPortletRetriever)
            self.__portlets = [self._dataToPortlet(a.data)
                                for a in self.filter(retriever.getPortlets())]
        return self.__portlets
    
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