from zope.component import getSiteManager
from plone.portlets.interfaces import IPortletType
from plone.portlets.registration import PortletType

def registerPortletType(site, title, description, addview, for_=None):
    """Register a new type of portlet.
    
    site should be the local site where the registration should be made. The 
    title and description should be meaningful metadata about the portlet for 
    the UI.
    
    The addview should be the name of an add view registered, and must be 
    unique.
    """
    sm = getSiteManager(site)
    
    portlet = PortletType()
    portlet.title = title
    portlet.description = description
    portlet.addview = addview
    portlet.for_ = for_
    
    sm.registerUtility(component=portlet, provided=IPortletType, name=addview)
    
def unregisterPortletType(site, addview):
    """Unregister a portlet type.
    
    site is the local site where the registration was made. The addview 
    should is used to uniquely identify the portlet.
    """
    
    sm = getSiteManager(site)
    sm.unregisterUtility(provided=IPortletType, name=addview)
