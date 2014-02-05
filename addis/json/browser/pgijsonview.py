from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from addis.json import jsonMessageFactory as _


class IPGIJsonView(Interface):
    """
    PGIJson view interface
    """



class PGIJsonView(BrowserView):
    """
    PGIJson browser view
    """
    implements(IPGIJsonView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

