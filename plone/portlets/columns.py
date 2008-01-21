from persistent.list import PersistentList
from persistent import Persistent
from zope.component import queryUtility
from plone.portlets.interfaces import IPortletManager


class ColumnManager(Persistent):

    def __init__(self):
        self.columns = PersistentList()

    def insert(self, name):
        self.columns.insert(0, name)

    def append(self, name):
        self.columns.append(name)

    def left(self, name):
        if name == self.columns[0]:
            return None
        else:
            current = self.columns.index(name)
            return self.columns[current-1]

    def right(self, name):
        if name == self.columns[-1]:
            return None
        else:
            current = self.columns.index(name)
            return self.columns[current+1]

    def move_portlet_to_column(self, portlet, column):
        """ This method needs to be implemented by the plone.app.portlet
            package. 
        """
        raise NotImplementedError
        

    def get_column_name_of(self, name):
        for column_name in self.columns:
            column = queryUtility(IPortletManager, column_name)
            # if name in column.getUserPortletAssignment()

    def __iter__(self):
        for column in self.columns:
            yield column
            
