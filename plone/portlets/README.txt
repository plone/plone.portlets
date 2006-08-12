=====================
Plone Portlets Engine
=====================

This package contains the basic interfaces and generalisable code for managing
dynamic portlets. Portlets are viewlets (see zope.viewlet) which are assigned to
columns or other areas (represented by a particular viewlet manager). 

The portlets infrastructure differs from zope.contentprovider and zope.viewlet
in that it is dynamic. Rather than register viewlets that "plug into" a viewlet
manager in ZCML, plone.portlets contains the basis for portlets that are 
assigned - persistently, at run time - to locations, users or groups.

The remainder of this file will explain the API and components in detail, but
in general, the package is intended to be used as follows:

- The application layer registers a generic adapter to IPortletContext. Any
context where portlets may be assigned needs to be adaptable to this interface.

- The application layer registers a local utility providing IPortletStorage.
This is so that portlets can be persistently assigned to contexts, users and
groups.

- An application will register a <browser:viewletManager> with 
PortletViewletManager in the list of bases for each column or location where
portlets should be rendered.

Actual portlets consist of two or three components, depending on the use case.

- A special type viewlet, IPortletViewlet, knows how to render each type of
portlet. The IPortletViewlet should be a multi-adapter from (context, request, 
view, viewlet manager, data).

- An IPortletAssignment is a persistent object that can be instantiated and
is stored by the IPortletStorage, managed by adapting an IPortletContext to
an IPortletManager. The assignment can return a handle to an 
IPortletDataProvider.

- The IPortletDataProvider is adapted (along other aspects of the context) to
a specific IPortletViewlet. For "specific-specific" portlets (see below) the
IPortletAssignment and IPortletDataProvider may well be part of the same object.

Typically, you will either have a specific IPortletAssignment for a specific
IPortletDataProvider, or a generic IPortletAssignment for different types of
IPortletDataProvider. The examples below demonstrate a "specific-specific"
portlet in the form of a login portlet - here, the same object provides both
the assignment and the data provider aspect - and a "generic-generic" portlet,
where a generic IPortletAssignment knows how to reference a content object,
with different content objects potentially having different types of 
IPortletViewlets for rendering.

Defining types of portlets
--------------------------

Portlets are rooted in a data provider. This could, for example, be a Smart 
Folder (aka "Topic") that canns a query, or an object holding static text to
render. Alternatively, the data provider can be "conceptual", where there is
no separate configuration data to be held. We will see an example of this
later, in the form of a login portlet.

Let's create a dummy data provider object to work on

  >>> from zope.interface import implements, Interface
  >>> from zope.component import adapts
  >>> from zope import schema
  
  >>> class ITestContent(Interface):
  ...     pass
  >>> class ITestDocument(ITestContent):
  ...     text = schema.TextLine(title=u"Text to render")
  >>> class TestDocument(object):
  ...     implements(ITestDocument)
  ...     text = ''
  
  >>> doc = TestDocument()
  >>> doc.text = "Some body text"
  
Suppose the user turned this into a portlet. This could happen by adding the
IPortletDataProvider marker interface. A type that was always a portlet data
provider would of course have this interface applied to its class always.
  
  >>> from plone.portlets.interfaces import IPortletDataProvider
  >>> from zope.interface import directlyProvides
  >>> directlyProvides(doc, IPortletDataProvider)

In order to be able to render this portlet, a viewlet adapter must exist for it.
Typically, an IPortletDataProvider (or a sub-interface thereof) and an
IPortletViewlet adapter will come as a pair.

  >>> from plone.portlets.interfaces import IPortletViewlet
  >>> from plone.portlets.interfaces import IPortletViewletManager
  >>> from zope.app.publisher.interfaces.browser import IBrowserView
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> from zope.viewlet.viewlet import ViewletBase
  
  >>> class TestDocumentViewlet(ViewletBase):
  ...     implements(IPortletViewlet)
  ...     adapts(Interface, IBrowserRequest, IBrowserView, 
  ...       IPortletViewletManager, ITestDocument)
  ... 
  ...     def __init__(self, context, request, view, manager, data):
  ...         super(TestDocumentViewlet, self).__init__(context, request, view, manager)
  ...         self.data = data
  ...
  ...     def render(self, *args, **kwargs):
  ...         return r'<p>%s</p>' % (self.data.text,)
  
  >>> from zope.app.testing.ztapi import provideAdapter
  >>> provideAdapter((Interface, IBrowserRequest, IBrowserView, 
  ...     IPortletViewletManager, ITestDocument), IPortletViewlet, TestDocumentViewlet)
  
The adapter registration for a viewlet is a bit hairy. It is necessary, however,
to give portlets all the context they need to be able to render themselves.
Specifically, it adapts:

 - The current context content object where it is being rendered
 - The request
 - The current view where it is being rendered
 - The portlet viewlet manager it is being rendered in
 - The data provider as returned by IPortletAssignment.data
  
The viewlet manager will update() and render() each viewlet it is assigned,
a bit like this (see below for how to use the actual viewlet manager):
  
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> viewlet = TestDocumentViewlet(None, None, None, None, doc)
  >>> viewlet.update() # IViewlet contract says we should always call this first
  >>> viewlet.render()
  '<p>Some body text</p>'
  
  
Assigning portlets to contexts
------------------------------

In the example a above, TestDocument may have a purpose besides just being a
portlet. Other types of portlet may be more specific, but in general we cannot
rely on the actual portlet data being managed exclusively by the portlets
infrastructure. 

To determine which portlets are assigned where, an object providing
IPortletAssignment is needed. This will typically be persistent, and may be
generic for a given type of portlet. For example, if portlet data is to be
provided by content objects with a UID, a generic assignment type could be
provided for all such portlets. 

Before we can write this, however, we need to provide some more information
about the context where the portlet will be assigned. The context is
described in an IPortletContext, and typically a content object will be
adaptable to this interface.

Let's assume such content objects have a UID to identify them. In the real 
world, the UID may be looked up in a catalog or UID registry in order to 
obtain a real object. In this case, we will fake this with a global dict.

  >>> testUIDRegistry = {}
  
  >>> class ITestReferenceable(Interface):
  ...     uid = schema.TextLine(title=u'The UID of the item')
  
  >>> class TestContentLocator(object):
  ...     implements(ITestReferenceable)
  ...     adapts(ITestContent)
  ...     
  ...     def __init__(self, context):
  ...         self.context = context
  ...
  ...     @property
  ...     def uid(self):
  ...         return id(self.context)
  >>> provideAdapter(ITestContent, ITestReferenceable, TestContentLocator)
  
  >>> testUIDRegistry[id(doc)] = doc
  
Portlets can also be assigned to users and groups - we simply reference these 
from global variables for testing purposes.

  >>> testUser = 'TestUser'
  >>> testUserGroups = ('TestGroup1', 'TestGroup2',)

Now we can provide an IPortletContext for this environment:

  >>> from plone.portlets.interfaces import IPortletContext
  >>> class TestPortletContext(object):
  ...     implements(IPortletContext)
  ...     adapts(ITestContent)
  ...
  ...     def __init__(self, context):
  ...         self.context = context
  ...
  ...     @property
  ...     def uid(self):
  ...         return ITestReferenceable(self.context).uid
  ...
  ...     @property
  ...     def parent(self):
  ...         return None # Dont' implement parentage yet
  ...
  ...     @property
  ...     def userId(self):
  ...         return testUser
  ...
  ...     @property
  ...     def groupIds(self):
  ...         return testUserGroups
  >>> provideAdapter(ITestContent, IPortletContext, TestPortletContext)
  
We can also provide a generic IPortletAssignment for any content object
that is in this environment. This assignment type will be initialised with a 
reference to a content object (such as our TestDocument above), but it will 
store only the location (UID) of this object.
  
  >>> from plone.portlets.interfaces import IPortletAssignment
  >>> from persistent import Persistent
  
  >>> class TestReferenceablePortletAssignment(Persistent):
  ...     implements(IPortletAssignment)
  ...
  ...     def __init__(self, id, content):
  ...         location = ITestReferenceable(content)
  ...         self._id = id
  ...         self._uid = location.uid
  ...
  ...     @property
  ...     def id(self):
  ...         return self._uid
  ...
  ...     @property
  ...     def data(self):
  ...         return testUIDRegistry[self._uid]
  
Other assignment implementations may well co-exist with this one. Consider
a case where a portlet can be assigned to a context without referencing a
configuration object:

  >>> class ILoginPortlet(IPortletDataProvider):
  ...   pass
  >>> class TestLoginPortletAssignment(Persistent):
  ...     implements(IPortletAssignment, ILoginPortlet)
  ...     
  ...     @property
  ...     def data(self):
  ...         return self
  >>> class TestLoginPortletViewlet(ViewletBase):
  ...     implements(IPortletViewlet)
  ...     adapts(Interface, IBrowserRequest, IBrowserView, 
  ...             IPortletViewletManager, ILoginPortlet)
  ... 
  ...     def __init__(self, context, request, view, manager, data):
  ...         super(TestDocumentViewlet, self).__init__(context, request, view, manager)
  ...         self.data = data
  ...
  ...     def update(self):
  ...         pass
  ...
  ...     def render(self, *args, **kwargs):
  ...         return r'<form action="/login">...</form>'
  
  >>> provideAdapter((Interface, IBrowserRequest, IBrowserView, \
  ...   IPortletViewletManager, ILoginPortlet), IPortletViewlet, TestLoginPortletViewlet)
  
Now, assume we wanted to assign some portlets to a particular folder:
  
  >>> class TestFolder(object):
  ...     implements(ITestContent)
  >>> folder = TestFolder()
  >>> testUIDRegistry[id(folder)] = folder

We can adapt this to an IPortletContext:

  >>> folderPortletContext = IPortletContext(folder)
  >>> folderPortletContext
  <TestPortletContext object at ...>
  
The UI will now be able to adapt this context to an IPortletManager, which 
provides methods for adding and removing portlet assignments relative to this
context.

  >>> from plone.portlets.interfaces import IPortletManager
  >>> portletManager = IPortletManager(folderPortletContext)
  >>> portletManager
  <plone.portlets.manager.DefaultPortletManager object at ...>

The portlet manager will delegate actual storage of the assignments to a (local) 
utility providing IPortletStorage. A volatile and generic global portlet storage
utility is provided in this package.

  >>> from zope.component import getUtility
  >>> from plone.portlets.interfaces import IPortletStorage
  >>> volatileStorage = getUtility(IPortletStorage)
  >>> volatileStorage
  <plone.portlets.storage.VolatilePortletStorage object at ...>
  
Portlets are assigned to a particular viewlet manager (representing e.g. a
column). We will describe these in detail later, but for now, let's just
create one so that we can demonstrate the assignment:

  >>> from plone.portlets.viewletmanager import PortletViewletManager
  >>> columnOne = PortletViewletManager(folder, request, None)
  
With this, we can assign a portlet based on our test document to the folder.

  >>> docAssignment = TestReferenceablePortletAssignment('portlet.doc', doc)
  >>> portletManager.setPortletAssignments(columnOne, [docAssignment])
  
  >>> portletManager.getPortletAssignments(columnOne)
  [<TestReferenceablePortletAssignment object at ...>]
  >>> portletManager.getPortletAssignments(columnOne)[0] == docAssignment
  True
  
  >>> folderUID = ITestReferenceable(folder).uid
  >>> volatileStorage.getPortletAssignmentsForContext(columnOne, folderUID)
  [<TestReferenceablePortletAssignment object at ...>]
  >>> volatileStorage.getPortletAssignmentsForContext(columnOne, folderUID)[0] == docAssignment
  True

Notice that the IPortletStorage also knows assignments for users and groups.
These may be managed by IPortletManagers adapting user and group objects. For
testing purposes, we will simply assign these manually.

  >>> loginPortlet = TestLoginPortletAssignment()
  >>> volatileStorage.setPortletAssignmentsForUser(columnOne, testUser, [loginPortlet])
  >>> volatileStorage.getPortletAssignmentsForUser(columnOne, testUser)
  [<TestLoginPortletAssignment object at ...>]
  >>> volatileStorage.getPortletAssignmentsForUser(columnOne, testUser)[0] == loginPortlet
  True
  
  >>> groupDoc = TestDocument()
  >>> groupDoc.text = 'Group specific text'
  >>> groupDocAssignment = TestReferenceablePortletAssignment('portlet.group', groupDoc)
  >>> volatileStorage.setPortletAssignmentsForGroup(columnOne, testUserGroups[0], [groupDocAssignment])
  >>> volatileStorage.getPortletAssignmentsForGroup(columnOne, testUserGroups[0])
  [<TestReferenceablePortletAssignment object at ...>]
  >>> volatileStorage.getPortletAssignmentsForGroup(columnOne, testUserGroups[0])[0] == groupDocAssignment
  True

Rendering portlets
------------------

UNRESOLVED:
      - Storage can't use manager *instance* as key - needs id/name
      - Can VolatilePortletStorage be made optionally persistent?

TODO: 
      - Tests for viewlet manager + retriever
