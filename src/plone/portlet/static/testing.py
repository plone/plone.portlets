from plone.app.testing import applyProfile
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig


class PlonePortletStaticLayer(PloneSandboxLayer):
    def setUpZope(self, app, configurationContext):
        import plone.portlet.static

        xmlconfig.file(
            "configure.zcml", plone.portlet.static, context=configurationContext
        )

    def setUpPloneSite(self, portal):
        applyProfile(portal, "plone.portlet.static:default")


PLONEPORTLETSTATIC_FIXTURE = PlonePortletStaticLayer()

PLONEPORTLETSTATIC_INTEGRATION_TESTING = IntegrationTesting(
    bases=(PLONEPORTLETSTATIC_FIXTURE,), name="PloneAppCollectionLayer:Integration"
)
