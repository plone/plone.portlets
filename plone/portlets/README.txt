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

Let's create a dummy content object to work on

  >>> from zope.interface import implements, Interface
  >>> from zope.component import adapts
  >>> from zope import schema
  
  >>> class ITestDocument(Interface):
  ...     text = schema.TextLine(title=u"Text to render")
  >>> class TestDocument(object):
  ...     implements(ITestDocument)
  ...     text = ''
  
  >>> doc = TestDocument()
  >>> doc.text = "Some body text"
  
Suppose the user turned this into a portlet. This could happen by adding the
IPortletDataProvider marker interface.
  
  >>> from plone.portlets.interfaces import IPortletDataProvider
  >>> from zope.interface import directlyProvides
  >>> directlyProvides(doc, IPortletDataProvider)

In order to be able to render this portlet, a viewlet adapter must exist for it.
Typically, an IPortletDataProvider (or a sub-interface thereof) and an
IPortletViewlet will come as a pair.

  >>> from plone.portlets.interfaces import IPortletViewlet
  >>> class TestDocumentViewlet(object):
  ...     implements(IPortletViewlet)
  ...     adapts(ITestDocument)
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
  >>> provideAdapter(ITestDocument, IPortletViewlet, TestDocumentViewlet)
  
The viewlet manager will update() and render() each viewlet it is assigned,
much like this (see below):
  
  >>> from zope.publisher.browser import TestRequest
  >>> request = TestRequest()
  >>> viewlet = TestDocumentViewlet(doc, request)
  >>> viewlet.update()
  >>> viewlet.render()
  '<p>Some body text</p>'
  
Assigning viewlets to contexts
------------------------------

In the example a above, TestDocument may have a purpose besides just being a
portlet. Other types of portlet may be more specific, but in general we cannot
rely on the actual portlet data being managed exclusively by the portlets
infrastructure. 

To determine which portlets are assigned where, an object providing
IPortletAssignment is needed. This will typically be persistent, and may be
generic for a given type of portlet. For example, if portlet data is to be
provided by content objects with a UID, a generic assignments type could be
provided for all such portlets. 

In the real world, the UID may be looked up in a catalog or UID registry in 
order to obtain a real object. In this case, we will fake this with a global
dict.

  >>> testUIDRegistry = {}
  
  >>> class ITestReferenceableContent(Interface):
  ...     uid = schema.TextLine(title=u'The UID of the item')
  
  >>> class TestDocumentLocator(object):
  ...     implements(ITestReferenceableContent)
  ...     adapts(ITestDocument)
  ...     
  ...     def __init__(self, context):
  ...         self.context = context
  ...
  ...     @property
  ...     def uid(self):
  ...         return id(self.context)
  >>> provideAdapter(ITestDocument, ITestReferenceableContent, TestDocumentLocator)
  
  >>> testUIDRegistry[id(doc)] = doc
  
  >>> from plone.portlets.interfaces import IPortletAssignment
  >>> from persistent import Persistent
  
  >>> class TestReferenceableContentPortletAssignment(Persistent):
  ...     implements(IPortletAssignment)
  ...
  ...     def __init__(self, content):
  ...         location = ITestReferenceableContent(content)
  ...         self.uid = location.uid
  ...
  ...     @property
  ...     def data(self):
  ...         return testUIDRegistry[self.uid]
  
This slightly contrived example just shows that the IPortletAssignment
implementation is persistent and can be used as a lightweight pointer to
the actual data provider.

It is implied in the contract to IPortletAssignment that the data object it
locates can be adapted to IPortletViewlet in order to render it. We will
see how the viewlet manager does this later.


