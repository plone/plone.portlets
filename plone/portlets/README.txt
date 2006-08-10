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

Defining types of portlets
--------------------------

Portlets are rooted in a data provider. This could, for example, be a Smart 
Folder (aka "Topic") that canns a query, or an object holding static text to
render. The use of a data provider isn't strictly necessary, but will be the 
most common case.

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
IPortletDataProvider marker interface (a type that was always a portlet data
provider would of course have this interface applied to its class always).
  
  >>> from plone.portlets.interfaces import IPortletDataProvider
  >>> from zope.interface import directlyProvides
  >>> directlyProvides(doc, IPortletDataProvider)

In order to be able to render this portlet, a viewlet adapter must exist for it.
Typically, an IPortletDataProvider (or a sub-interface thereof) and an
IPortletViewlet adapter will come as a pair.

  >>> from plone.portlets.interfaces import IPortletViewlet
  >>> from zope.publisher.interfaces.browser import IBrowserRequest
  >>> class TestDocumentViewlet(object):
  ...     implements(IPortletViewlet)
  ...     adapts(ITestDocument, IBrowserRequest)
  ... 
  ...     def __init__(self, context, request):
  ...         self.__parent__ = None
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def update(self):
  ...         pass
  ...
  ...     def render(self, *args, **kwargs):
  ...         return r'<p>%s</p>' % (self.context.text,)
  
  >>> from zope.app.testing.ztapi import provideAdapter
  >>> provideAdapter((ITestDocument, IBrowserRequest), IPortletViewlet, TestDocumentViewlet)
  
The viewlet manager will update() and render() each viewlet it is assigned,
much like this (see below for how to use the actual viewlet manager):
  
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> viewlet = TestDocumentViewlet(doc, request)
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
that is in to this environment. This assignment type will be initialised 
with a reference to a content object (such as our TestDocument above), but it
will store only the location (UID) of this object.
  
  >>> from plone.portlets.interfaces import IPortletAssignment
  >>> from persistent import Persistent
  
  >>> class TestReferenceablePortletAssignment(Persistent):
  ...     implements(IPortletAssignment)
  ...
  ...     def __init__(self, content):
  ...         location = ITestReferenceable(content)
  ...         self.uid = location.uid
  ...
  ...     @property
  ...     def data(self):
  ...         return testUIDRegistry[self.uid]
  
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
  >>> class TestLoginPortletViewlet(object):
  ...     implements(IPortletViewlet)
  ... 
  ...     def __init__(self, context, request):
  ...         self.__parent__ = None
  ...         self.context = context
  ...         self.request = request
  ...
  ...     def update(self):
  ...         pass
  ...
  ...     def render(self, *args, **kwargs):
  ...         return r'<form action="/login">...</form>'
  
  >>> provideAdapter((ILoginPortlet, IBrowserRequest), IPortletViewlet, TestLoginPortletViewlet)
  
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

The portlet manager will delegate actual storage to of the assignments to
a (local) utility providing IPortletStorage. A volatile and generic global
portlet storage utility is provided in this package.

  >>> from zope.component import getUtility
  >>> from plone.portlets.interfaces import IPortletStorage
  >>> volatileStorage = getUtility(IPortletStorage)
  >>> volatileStorage
  <plone.portlets.storage.VolatilePortletStorage object at ...>
  
Portlets are assigned to a particular viewlet manager (representing e.g. a
column). We will describe these in detail later, but for now, let's just
create one so that we can demonstrate the assignment:

  >>> from plone.portlets.viewletmanager import PortletViewletManager
  >>> columnOne = PortletViewletManager()
  
With this, we can assign a portlet based on our test document to the folder.

  >>> docAssignment = TestReferenceablePortletAssignment(doc)
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
  >>> groupDocAssignment = TestReferenceablePortletAssignment(groupDoc)
  >>> volatileStorage.setPortletAssignmentsForGroup(columnOne, testUserGroups[0], [groupDocAssignment])
  >>> volatileStorage.getPortletAssignmentsForGroup(columnOne, testUserGroups[0])
  [<TestReferenceablePortletAssignment object at ...>]
  >>> volatileStorage.getPortletAssignmentsForGroup(columnOne, testUserGroups[0])[0] == groupDocAssignment
  True

Rendering portlets
------------------

TODO: - Finish IPortletRetriever, write test
      - Implement the viewlet manager w/ tests for rendering
      - Evaluate whether VolatilePortletStorage can be made optionally persistent
      