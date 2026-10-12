from AccessControl.Permission import addPermission
from zope.i18nmessageid import MessageFactory

PloneMessageFactory = MessageFactory("plone")

addPermission(
    "plone.portlet.static: Add static portlet",
    (
        "Manager",
        "Site Administrator",
        "Owner",
    ),
)
