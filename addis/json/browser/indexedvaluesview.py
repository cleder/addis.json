#
import simplejson as json

from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from addis.json import jsonMessageFactory as _


class IIndexedValuesView(Interface):
    """
    IndexedValues view interface
    """


class IndexedValuesView(BrowserView):
    """
    IndexedValues browser view
    """
    implements(IIndexedValuesView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    def __call__(self):
        self.request.RESPONSE.setHeader('Content-Type','application/json; charset=utf-8')
        catalog = self.portal_catalog
        indexes=[]
        for idx in catalog.Indexes.keys():
            try:
                mt = catalog.Indexes[idx].meta_type
            except:
                mt = None
            if mt in ['KeywordIndex', 'FieldIndex']:
                indexes.append({'name': idx, 'type': mt,
                                'values': catalog.uniqueValuesFor(idx)})
            elif mt is None:
                indexes.append({'name': idx, 'type': 'fulltext'})
            else:
                indexes.append({'name': idx, 'type': mt})
        return json.dumps(indexes)




