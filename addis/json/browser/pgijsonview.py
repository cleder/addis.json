#

import simplejson as json
import time
from ZODB.POSException import ConflictError
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from addis.json import jsonMessageFactory as _

def quotestring(s):
    return '"%s"' % s

def quotequery(s):
    if not s:
        return s
    try:
        terms = s.split()
    except ConflictError:
        raise
    except:
        return s
    tokens = ('OR', 'AND', 'NOT')
    s_tokens = ('OR', 'AND')
    check = (0, -1)
    for idx in check:
        if terms[idx].upper() in tokens:
            terms[idx] = quotestring(terms[idx])
    for idx in range(1, len(terms)):
        if (terms[idx].upper() in s_tokens and
            terms[idx-1].upper() in tokens):
            terms[idx] = quotestring(terms[idx])
    return ' '.join(terms)

def quote_bad_chars(s):
    """
    We need to quote parentheses when searching text indices (we use
    quote_logic_indexes as the list of text indices)
    """
    bad_chars = ["(", ")"]
    for char in bad_chars:
        s = s.replace(char, quotestring(char))
    return s

def build_query(context, request, show_all=True, quote_logic=False,
                quote_logic_indexes=['SearchableText','Description','Title'],):
    show_query = show_all
    results=[]
    catalog=getToolByName(context, 'portal_catalog')
    indexes=catalog.indexes()
    query={}
    second_pass = {}

    # See http://dev.plone.org/plone/ticket/9422 for
    # an explanation of '\u3000'
    multispace = u'\u3000'.encode('utf-8')

    # Avoid creating a session implicitly.
    for k in request.keys():
        if k in ('SESSION',):
            continue
        v = request.get(k)
        if v and k in indexes:
            if k in quote_logic_indexes:
                v = quote_bad_chars(v)
                if multispace in v:
                    v = v.replace(multispace, ' ')
                if quote_logic:
                    v = quotequery(v)
            query[k] = v
            show_query = True
        elif k.endswith('_usage'):
            key = k[:-6]
            param, value = v.split(':')
            second_pass[key] = {param:value}
        elif k in ('sort_on', 'sort_order', 'sort_limit'):
            if k == 'sort_limit' and not (type(v)==type(0)):
                query[k] = int(v)
            else:
                query[k] = v

    for k, v in second_pass.items():
        qs = query.get(k)
        if qs is None:
            continue
        query[k] = q = {'query':qs}
        q.update(v)

    return query, show_query


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

    def __call__(self):
        def missing(a):
            if a:
                return a
        t = time.time()
        result_list = []
        query, show_query = build_query(self.context, self.request)
        query['portal_type'] = 'ProjectGeneralInformation'
        search_results = self.portal_catalog(**query)
        for result in search_results:
            result_list.append({
                "DatabaseID": missing(result.getDatabaseID),
                "title": missing(result.Title),
                "ProjectTitle": missing(result.getProjectTitle),
                "FocalAreas": missing(result.getFocalAreas),
                "GEFPhase": missing(result.getGEFPhase),
                "Scope": missing(result.getScope),
                "ScopeOther": missing(result.getScopeOther),
                "Region": missing(result.getRegion),
                "SubRegion": missing(result.getSubRegion),
                "Countries": missing(result.getCountries),
                "LeadAgency": missing(result.getLeadAgency),
                "ExecutingAgencies": missing(result.getExecutingAgencies),
                "GEFid": missing(result.getGEFid),
                "url": result.getURL(),
            })
        return json.dumps({"results": result_list,
                        "metadata":{"duration": time.time() -t,
                                    "query": query,
                                    "totalresults": len(search_results)}
                            })

class PGIFullJsonView(PGIJsonView):

    def __call__(self):
        def missing(a):
            if a:
                return a
        t = time.time()
        result_list = []
        query, show_query = build_query(self.context, self.request)
        query['portal_type'] = 'ProjectGeneralInformation'
        search_results = self.portal_catalog(**query)
        for result in search_results:
            obj = result.getObject()
            try:
                gef_alloc = str(obj.getTotalGEFAllocation())
            except:
                gef_alloc = 'Error computing GEF Allocation'
            try:
                unep_alloc = str(obj.getTotalUNEPAllocation())
            except:
                unep_alloc = 'Error computing UNEP Allocation'
            result_list.append({
                "DatabaseID": missing(result.getDatabaseID),
                "title": missing(result.Title),
                "ProjectTitle": missing(result.getProjectTitle),
                "FocalAreas": missing(result.getFocalAreas),
                "GEFPhase": missing(result.getGEFPhase),
                "description": obj.getSummaryDescription(),
                "Scope": missing(result.getScope),
                "ScopeOther": missing(result.getScopeOther),
                "Region": missing(result.getRegion),
                "SubRegion": missing(result.getSubRegion),
                "Countries": missing(result.getCountries),
                "LeadAgency": missing(result.getLeadAgency),
                "ExecutingAgencies": missing(result.getExecutingAgencies),
                "GEFid": missing(result.getGEFid),
                "url": result.getURL(),
                "TaskManager": obj.getCurrentTM(),
                #"Year": missing(result.getYear),
                #'Status':
                "TotalGEFAllocation": gef_alloc,
                "TotalUNEPAllocation": unep_alloc,
                #"tags": missing(result.Subject),
            })
        return json.dumps({"results": result_list,
                        "metadata":{"duration": time.time() -t,
                                    "query": query,
                                    "totalresults": len(search_results)}
                            })

