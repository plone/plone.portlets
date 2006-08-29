from zope.interface import implements
from zope.app.container.sample import SampleContainer

from persistent import Persistent
from persistent.list import PersistentList

from BTrees.OOBTree import OOBTree

from plone.portlets.interfaces import IPortletStorage
from plone.portlets.interfaces import IPortletCategoryMapping
from plone.portlets.interfaces import IPortletAssignmentMapping

class PortletStorage(SampleContainer, Persistent):
    """The default portlet storage.
    """
    implements(IPortletStorage)

    def _newContainerData(self):
        return OOBTree()
        
class PortletCategoryMapping(SampleContainer, Persistent):
    """The default category/key mapping storage.
    """
    implements(IPortletCategoryMapping)

    __name__ = __parent__ = None

    def _newContainerData(self):
        return OOBTree()
        
class PortletAssignmentMapping(Persistent):
    """The default assignment mapping storage.
    """
    implements(IPortletAssignmentMapping)
    
    __name__ = __parent__ = None
    
    def __init__(self):
        self._assignments = self._newData()
        
    def keys(self):
        return range(len(self._assignments))

    def __iter__(self):
        return iter(self.keys())

    def __getitem__(self, key):
        return self._assignments[self._key(key)]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def values(self):
        return [a for a in self._assignments]

    def __len__(self):
        return len(self._assignments)

    def items(self):
        items = []
        idx = 0
        for a in self._assignments:
            items.append((idx, a))
            idx += 1
        return items

    def __contains__(self, key):
        try:
            key = self._key(key)
        except KeyError:
            return False
        return bool(key >= 0 and key < len(self._assignments))

    has_key = __contains__
    
    def __delitem__(self, key):
        key = self._key(key)
        assignment = self._assignments[key]
        del self._assignments[key]
        
        assignment.__parent__ = None
        assignment.__name__ = None
        
        self._reassignNames()
        
    def saveAssignment(self, assignment):
        key = getattr(assignment, '__name__', None)
        try:
            key = self._key(key)
        except KeyError:
            key = None
        if key is not None:
            self._assignments[key] = assignment
        else:
            key = len(self._assignments)
            assignment.__name__ = str(key)
            self._assignments.append(assignment)
            
        assignment.__parent__ = self
        
    def moveAssignment(self, key, idx):
        key = self._key(key)
        
        if idx < 0 or idx >= len(self._assignments):
            raise IndexError, idx
        
        assignment = self._assignments[key]
        del self._assignments[key]
        self._assignments.insert(idx, assignment)
        
        self._reassignNames()
        
    def _newData(self):
        return PersistentList()
        
    def _reassignNames(self):
        for idx in range(len(self._assignments)):
            self._assignments[idx].__name__ = str(idx)
    
    def _key(self, key):
        """Make the key into an int. If conversion fails, raise KeyError,
        not ValueError (since it means we were passed a bogus key).
        """
        try:
            key = int(key)
        except (ValueError, TypeError,):
            raise KeyError, key
        if key < 0 or key >= len(self._assignments):
            raise KeyError, key
        return key