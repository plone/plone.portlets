from persistent.dict import PersistentDict
from plone.portlets.constants import ASSIGNMENT_SETTINGS_KEY
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletAssignmentSettings
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.component import queryAdapter
from zope.container.contained import Contained
from zope.interface import implementer


@implementer(IPortletAssignmentSettings)
class PortletAssignmentSettings(Contained):
    def __init__(self):
        self.data = PersistentDict()

    def __setitem__(self, name, value):
        self.data[name] = value

    def __delitem__(self, name):
        del self.data[name]

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def get(self, name, default=None):
        return self.data.get(name, default)


@adapter(IPortletAssignment)
@implementer(IPortletAssignmentSettings)
def portletAssignmentSettingsFactory(context):
    annotations = queryAdapter(context, IAnnotations)
    settings = annotations.get(ASSIGNMENT_SETTINGS_KEY, None)

    if settings is None:
        settings = annotations[ASSIGNMENT_SETTINGS_KEY] = PortletAssignmentSettings()

    return settings
