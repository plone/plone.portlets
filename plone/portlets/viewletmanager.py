from zope.interface import implements

from interfaces import IPortletViewletManager
from interfaces import IPortletRetriever

class PortletViewletManager(object):
    """Default implementation of the viewlet manager
    """
    
    implements(IPortletViewletManager)
    
    # TODO: Implement the full interface
    
    def update(self):
        pass
        
    def render(self):
        pass