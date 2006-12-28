from zope.interface import implements, Interface
from zope.component import adapts
from zope.annotation.interfaces import IAnnotations

from plone.portlets.interfaces import IPortletContext
from plone.portlets.interfaces import ILocalPortletAssignable
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPlacelessPortletManager
from plone.portlets.interfaces import IPortletRetriever

from plone.portlets.constants import CONTEXT_ASSIGNMENT_KEY
from plone.portlets.constants import CONTEXT_BLACKLIST_STATUS_KEY

from plone.portlets.constants import CONTEXT_CATEGORY

class PortletRetriever(object):
    """The default portlet retriever.

    This will examine the context and its parents for contextual portlets,
    provided they provide ILocalPortletAssignable.
    """

    implements(IPortletRetriever)
    adapts(Interface, IPortletManager)

    def __init__(self, context, storage):
        self.context = context
        self.storage = storage

    def getPortlets(self):
        pcontext = IPortletContext(self.context, None)
        if pcontext is None:
            return []
            
        categories = [] # holds a list of (category, key, assignment)
        blacklisted = {}
        manager = self.storage.__name__
        
        # Get all global mappings - we will apply the blacklist later. Note
        # that the blacklist is tri-state; if it's None it means no assertion
        # has been made (i.e. the category has neither been whitelisted or
        # blacklisted by this object or any parent). The first item to give
        # either a blacklisted (True) or whitelisted (False) value for a given
        # item will set the appropriate value. Parents of this item that also
        # set a black- or white-list value will then be ignored.
        
        for category, key in pcontext.globalPortletCategories(False):
            mapping = self.storage.get(category, None)
            if mapping is not None:
                for a in mapping.get(key, {}).values():
                    categories.append((category, key, a,))
            blacklisted[category] = None
        
        # Get contextual portlets and black/white listings if possible. 
        # Note that not every parent may be an ILocalPortletAssignable, in 
        # which case we simply skip past this parent.
        
        current = self.context
        currentpc = pcontext
        contextAssignments = []
        parentBlacklisted = False
        
        while current is not None and currentpc is not None and not parentBlacklisted:
            assignable = ILocalPortletAssignable(current, None)
            if assignable is not None:
                annotations = IAnnotations(assignable)
                
                local = annotations.get(CONTEXT_ASSIGNMENT_KEY, None)
                if local is not None:
                    localManager = local.get(manager, None)
                    if localManager is not None:
                        contextAssignments.extend([(CONTEXT_CATEGORY, currentpc.uid, a) for a in localManager.values()])
                
                blacklistStatus = annotations.get(CONTEXT_BLACKLIST_STATUS_KEY, {}).get(manager, None)
                if blacklistStatus is not None:
                    for cat, status in blacklistStatus.items():
                        # Ensure we only get most specific blacklist status,
                        # and treat blacklisting of context portlets from parent
                        # as a special case.
                        if cat == CONTEXT_CATEGORY:
                            if status == True:
                                parentBlacklisted = True
                        elif blacklisted.get(cat, False) is None:
                            blacklisted[cat] = status
            
            # Check the parent - if there is no parent, we will stop
            current = currentpc.getParent()
            if current is not None:
                currentpc = IPortletContext(current, None)
        
        categories = contextAssignments + categories
        
        assignments = []
        for category, key, assignment in categories:
            # If there was no blacklisting information, or this was explicitly
            # *not* blacklisted, add to the list of assignments
            if blacklisted.get(category, None) is None or blacklisted[category] == False:
                assignments.append({'category'    : category,
                                    'key'         : key,
                                    'name'        : assignment.__name__,
                                    'assignment'  : assignment
                                    })
        return assignments
        
class PlacelessPortletRetriever(PortletRetriever):
    """A placeless portlet retriever.
    
    This will aggregate user portlets, then group portlets.
    """
    
    implements(IPortletRetriever)
    adapts(Interface, IPlacelessPortletManager)
    
    def __init__(self, context, storage):
        self.context = context
        self.storage = storage
        
    def getPortlets(self):
        pcontext = IPortletContext(self.context, None)
        if pcontext is None:
            return []
            
        assignments = []
        for category, key in pcontext.globalPortletCategories(True):
            mapping = self.storage.get(category, None)
            if mapping is not None:
                for assignment in mapping.get(key, {}).values():
                    assignments.append({'category'    : category,
                                        'key'         : key,
                                        'name'        : assignment.__name__,
                                        'assignment'  : assignment
                                        })
    
        return assignments