from zope.interface import implements
from zope.component import getMultiAdapter

from zope.viewlet.manager import ViewletManagerBase
import zope.security

from interfaces import IPortletContext
from interfaces import IPortletRetriever

from interfaces import IPortletViewletManager
from interfaces import IPortletViewlet

class PortletViewletManager(ViewletManagerBase):
    """Default implementation of the viewlet manager.
    """
    
    implements(IPortletViewletManager)

    def __init__(self, context, request, view):
        super(PortletViewletManager, self).__init__(context, request, view)

    def __getitem__(self, name):
        # Find the viewlet
        
        retriever = getMultiAdapter((IPortletContext(self.context), self), IPortletRetriever)
        assignment = retriever.getPortlet(self, name)
        ILoginPortlet, IBrowserRequest, IBrowserView, IPortletViewletManager
        viewlet = self.dataToPortlet(assignment.data)
    
        # If the viewlet was not found, then raise a lookup error
        if viewlet is None:
            raise ComponentLookupError('No viewlet with name `%s` found.' %name)

        # If the viewlet cannot be accessed, then raise an
        # unauthorized error
        if not zope.security.canAccess(viewlet, 'render'):
            raise zope.security.interfaces.Unauthorized(
                'You are not authorized to access the provider '
                'called `%s`.' %name)

        # Return the viewlet.
        return viewlet

    def sort(self, viewlets):
        # We sort them the way they are presented by the retreiver
        return viewlets

    def update(self):
        self.__updated = True

        retriever = getMultiAdapter((IPortletContext(self.context), self), IPortletRetriever)
        assignments = retriever.getPortlets(self)
        viewlets = [(a.id, self.dataToPortlet(a.data)) for a in assignments]
        
        viewlets = self.filter(viewlets)
        viewlets = self.sort(viewlets)

        # Just use the viewlets from now on
        self.viewlets = [viewlet for name, viewlet in viewlets]

        # Update all viewlets
        [viewlet.update() for viewlet in self.viewlets]
        
    def dataToPortlet(self, data):
        """Helper method to get the correct IPortletViewlet for the given
        data object.
        """
        return getMultiAdapter((self.context, self.request, self.view, 
                                    self, assignment.data,), IPortletViewlet)