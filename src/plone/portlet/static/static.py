from Acquisition import aq_inner
from plone.app.portlets.portlets import base
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.app.z3cform.widgets.richtext import RichTextFieldWidget
from plone.autoform import directives
from plone.base.utils import safe_text
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.portlet.static import PloneMessageFactory as _
from plone.portlets.interfaces import IPortletDataProvider
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import getUtility
from zope.interface import implementer

import logging
import re

logger = logging.getLogger("plone.portlet.static")


class IStaticPortlet(IPortletDataProvider):
    """A portlet which renders predefined static HTML.

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    header = schema.TextLine(
        title=_("Portlet header"),
        description=_("Title of the rendered portlet"),
        constraint=re.compile(r"[^\s]").match,
        required=False,
    )

    directives.widget(text=RichTextFieldWidget)
    text = RichText(title=_("Text"), description=_("The text to render"), required=True)

    omit_border = schema.Bool(
        title=_("Omit portlet border"),
        description=_(
            "Tick this box if you want to render the text above "
            "without the standard header, border or footer."
        ),
        required=False,
        default=False,
    )

    footer = schema.TextLine(
        title=_("Portlet footer"),
        description=_("Text to be shown in the footer"),
        required=False,
    )

    more_url = schema.ASCIILine(
        title=_("Details link"),
        description=_("If given, the header and footer will link to this URL."),
        required=False,
    )


@implementer(IStaticPortlet)
class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    header = _("title_static_portlet", default="Static text portlet")
    text = ""
    omit_border = False
    footer = ""
    more_url = ""

    def __init__(self, header="", text="", omit_border=False, footer="", more_url=""):
        self.header = header
        self.text = text
        self.omit_border = omit_border
        self.footer = footer
        self.more_url = more_url

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave or
        static string if title not defined.
        """
        return self.header or _("portlet_static", default="Static Portlet")


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile("static.pt")

    def css_class(self):
        """Generate a CSS class from the portlet header"""
        header = self.data.header
        if header:
            normalizer = getUtility(IIDNormalizer)
            return "portlet-static-%s" % normalizer.normalize(header)
        return "portlet-static"

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)

    def transformed(self, mt="text/x-html-safe"):
        """Use the safe_html transform to protect text output. This also
        ensures that resolve UID links are transformed into real links.
        """
        orig = self.data.text
        context = aq_inner(self.context)

        if isinstance(orig, RichTextValue):
            orig = orig.raw

        if not isinstance(orig, str):
            # Apply a potentially lossy transformation, and hope we stored
            # utf-8 text. There were bugs in earlier versions of this portlet
            # which stored text directly as sent by the browser, which could
            # be any encoding in the world.
            orig = safe_text(orig)
            logger.warn(
                "Static portlet at %s has not stored text/unicode. "
                "Assuming utf-8 encoding." % context.absolute_url()
            )

        transformer = getToolByName(context, "portal_transforms")
        transformer_context = context
        if hasattr(self, "__portlet_metadata__"):
            if (
                "category" in self.__portlet_metadata__
                and self.__portlet_metadata__["category"] == "context"
            ):
                assignment_context_path = self.__portlet_metadata__["key"]
                assignment_context = context.unrestrictedTraverse(
                    assignment_context_path
                )
                transformer_context = assignment_context
        data = transformer.convertTo(
            mt, orig, context=transformer_context, mimetype="text/html"
        )
        result = data.getData()
        if result:
            return safe_text(result)
        return None


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The create() method actually
    constructs the assignment that is being added.
    """

    schema = IStaticPortlet

    label = _("title_add_static_portlet", default="Add static text portlet")
    description = _(
        "description_static_portlet",
        default="A portlet which can display static HTML text.",
    )

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form

    This is registered in configure.zcml.
    """

    schema = IStaticPortlet

    label = _("title_edit_static_portlet", default="Edit static text portlet")
    description = _(
        "description_static_portlet",
        default="A portlet which can display static HTML text.",
    )
