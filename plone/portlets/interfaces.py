from zope.interface import Interface, Attribute
from zope import schema

from zope.annotation.interfaces import IAttributeAnnotatable

from zope.app.container.interfaces import IContained, IContainer, IReadContainer
from zope.app.container.constraints import containers, contains
from zope.contentprovider.interfaces import IContentProvider
from zope.interface.common.mapping import IReadMapping

# Context - the application layer must provide these    

class ILocalPortletAssignable(IAttributeAnnotatable):
    """Marker interface for content objects that want to have local portlet
    assignments.
    """

class IPortletContext(Interface):
    """A context in which portlets may be rendered.
    
    No default implementation exists for this interface - it must be provided
    by the application in order to tell the portlets infrastructure how to
    render portlets.
    """
    
    def getParent():
        """Get the portlet parent of the current context.
        
        This is used to aggregate portlets by walking up the content hierarchy.
        
        This should be adaptable to IPortletContext. If there is no portlet
        parent (e.g. this is the site root), return None.
        """
    
    def globalPortletCategories(placeless=False):
        """Get global portlet key-value pairs, in order.
        
        When rendered, a portlet manger (column) will be filled first by
        contextual portlets (if the context and/or its parents provide
        ILocalPortletAssignable), and then by global portlets. Global portlet
        assignments may include portlets per user, per group, or per content
        type.
        
        This function should return a tuple of tuples where each inner tuple
        contains a category such as 'user' or 'group' and the key to use in
        this category. 
        
        For example, if the current content object is a 'Document', the current 
        user is 'fred' and he is a member of 'group1' and 'group2', this may
        be:
        
        (('content_type', 'Documment'),
         ('user', 'fred',),
         ('group', 'group1',),
         ('group', 'group2',),)
         
        In this case, all contextual portlets may be rendered first, followed
        by all global portlets in the content_type category assigned to 
        'Document', followed by user portlets for 'fred' and group portlets for
        'group1' and then 'group2'.
        
        If ``placeless`` is True, the categories should only include those 
        which are independent of the specific location. In this case, that
        may mean that the 'content_type' category is excluded.
        """
        
# Utility interface for registrations of available portlets

class IPortletType(Interface):
    """A registration for a portlet type.
    
    Each new type of portlet should register a utility with a unique name
    providing IPortletType, so that UI can find them.
    """
    
    title = schema.TextLine(
        title = u'Title',
        required = True)
   
    description = schema.Text(
        title = u'Description',
        required = False)

    addview = schema.TextLine(
        title = u'Add view',
        description = u'The name of the add view for assignments for this portlet type',
        required = True)
        
# Generic marker interface - a portlet may reference one of these

class IPortletDataProvider(Interface):
    """A marker interface for objects providing portlet data.
    
    This can be used as a marker by implementations requiring a regular content 
    object to be able to be "switched on" as a portlet. Alternatively, a more
    specific sub-interface can provide the necessary information to render
    the portlet.
    
    An adapter should exist from the specific type of IPortletDataProvider to 
    an appropriate IPortletViewlet to render it.
    
    The data provider will also be referenced in an IPortletAssignment so that
    it can be retrieved on demand.
    """

# Portlet assignment - new types of portlets may need one of these

class IPortletAssignment(IContained):
    """Assignment of a portlet to a given portlet manager relative to a 
    context, user or group.
    
    Implementations of this interface will typically be persistent, stored in
    an IPortletStorage.
    
    The 'data' attribute may be implemented as a property that retrieves the
    data object on-demand.
    
    Portlet assignments are contained in and will have their __name__ attribute
    managed by an IPortletContextMapping, which in turn are stored inside 
    IPortletStorages.
    """
    
    title = schema.Bool(title=u'Title',
                        description=u'The title of this assignment as displayed to the user',
                        required=True)
        
    available = schema.Bool(title=u'Available',
                            description=u'Whether or not this portlet shuld be rendered',
                            required=True,
                            readonly=True)
    
    data = Attribute(u'Portlet data object')
    
# A content provider capable of rendering portlets - each type of portlet will
# need one of these
    
class IPortletRenderer(IContentProvider):
    """A special implementation of a content provider which is managed
    by an IPortletManager.
    
    Any object providing IPortletDataProvider should be adaptable to 
    IPortletRenderer in order to be renderable as a portlet. (In fact,
    the return value of IPortletAssignment.data needs to have such an
    adapter, regardless of whether it actually implements IPortletDataProvider)
    """
    
# Discovery of portlets

class IPortletRetriever(Interface):
    """A component capable of discovering portlets assigned to it for rendering.
    
    Typically, a content object and an IPortletManager will be multi-
    adapted to IPortletRetriever.
    """

    def getPortlets():
        """Return a list of IPortletAssignment's to be rendered
        """

# Portlet managment

class IPortletStorage(IContainer):
    """A component for storing global (site-wide) portlet assignments.
    
    This manages one IPortletCategoryMapping for each category of portlet, 
    e.g. 'user' or 'group' (the exact keys are up to the application layer).
    
    Some common keys are found in plone.portlets.constants.
    """
    contains('plone.portlets.interfaces.IPortletCategoryMapping')            

class IPortletCategoryMapping(IContainer, IContained):
    """A mapping of the portlets assigned to a particular categories under
    various keys.
    
    This manages one IPortletAssignmentMapping for each key. For example,
    if this is the 'user' category, the keys could be user ids, each of
    which would be given a particular IPortletAssignmentMapping.
    """
    contains('plone.portlets.interfaces.IPortletAssignmentMapping')

class IPortletAssignmentMapping(IReadContainer, IContained):
    """A storage for portlet assignments.
    
    An IPortletCategoryMapping manages one of these for each category of 
    context.
    
    This is a read container, and so it can be iterated, etc. Keys are managed
    by the container, and so assignments should be added/updated with 
    saveAssignment() (there is no __setitem__). Once saved, an assignment will
    be given a __name__, which is the key used for the container operations.
    """
    contains('plone.portlets.interfaces.IPortletAssignment')

    def __delitem__(self, key):
        """Remove the given assignment.
        
        note: we are not using a write container because we don't want callers
        to use __setitem__, but rather use saveAssignment.
        """

    def saveAssignment(assignment):
        """Save the given assignment.
        
        If this assignment has not yet been added to this container, it will
        be appended to the list of portlets in this context.
        """
        
    def moveAssignment(key, idx):
        """Move the given assignment to the given index.
        """

class IPortletManager(IPortletStorage, IContained):
    """A manager for portlets.
    
    Typically, objects providing this interface will be persisted and used
    to manage portlet assignments. 
    """
    
    def __call__(context, request, view):
        """Act as an adapter factory.
        
        When called, should return an IPortletManagerRenderer for rendering 
        this portlet manager and its portlets.
        
        The IPortletManager instance will be registered as a site-local
        adapter factory that the component architecture will use when it
        looks up adapters in the handler for a TAL provider: expression.
        
        See zope.contentprovider for more.
        """

class IPlacelessPortletManager(IPortletManager):
    """A manager for placeless portlets.
    
    A placeless portlet manager is one which does not examine the context
    or the context's parent. This is achieved by way of a different adapter
    to IPortletRetriever.
    """

class IPortletManagerRenderer(IContentProvider):
    """A content provider for rendering a portlet manager.
    """
    
    template = Attribute(
        """A page template object to render the manager with.

        If given, this will be passed an option 'portlets' that is a list of
        the IPortletRenderer objects to render.
        
        If not set, the renderers will simply be called one by one, and their
        output will be concatenated, separated by newlines.
        """)

    visible = schema.Bool(title=u'Visible',
                          description=u'Whether or not this portlet manager (column) will be rendered at all',
                          required=True,
                          default=True)

    def filter(self, portlets):
        """Return a list of IPortletRenderer's to display that is a subset of
        the list of IPortletRenderer's passed in.
        """
        
class ILocalPortletAssignmentManager(IPortletAssignmentMapping):
    """A mapping of portlet assignments relative to a context.
    
    An ILocalPortletAssignable may be multi-adapted along with
    an IPortletManager to this interface, to manage portlets relative to
    that context.
    """
    
    def setBlacklistStatus(category, status):
        """Manage the blacklisting status of the given category.
        
        If status is None, the blacklist status will be obtained from a parent,
        defaulting to False. If status is False, the given portlet category 
        will always be eligible for display. If status is True, the given
        portlet category will always be blocked.
        
        Thus, call setBlacklistStatus('user', True) to always black out 'user'
        portlets in this context, or setBlacklistStatus('user', False) to 
        override any blacklisting done by a parent object. Calling
        setBlacklistStatus('user', None) will cause the status to be acquired
        from the parent instead (defaulting to no blacklisting).
        """
    
    def getBlacklistStatus(category):
        """Get the blacklisting status of the given category.
        
        Note that this only applies to the current context - the status is
        not inherited, and will default to None if not set.
        """