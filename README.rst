Introduction
============

The list of fields that we would like to display on UNEP-Live.

- Database ID
- Short Title
- UNEP Priority
- Focal Area
- GEF Phase
- Project Description
- Geographic Scope
- Other Geographic Scope
- Region
- Sub-Region
- Country
- Lead GEF Agency
- Task Manager
- Executing Agency
- Date/Year
- Status
- Project budget: (UNEP participation, GEF participation)


After installing this product you should update the indexes:

::

    brains=context.portal_catalog(portal_type="ProjectGeneralInformation")
    for brain in brains:
        obj = brain.getObject()
        print 'reindex: ', '/'.join(obj.getPhysicalPath())
        obj.reindexObject()
    return printed

You can access the json at the URL: `stite/@@pgijson_view` for the catalog
only query and `site/@@pgifulljson_view` for the full results which will
wake up the objects and is  about 2 orders of magnitude slower.

The views are invoked with query parameters in the form:
`site/@@pgijson_view?Index=some+value&anotherIndex=some+other+value`

You can view the available indexes and their values at `site/@@indexedvalues_view`
in JSON format.

KeywordIndexes and FieldIndexes can be queried for multiple values like
`getCountries:list=Uganda&getCountries:list=Kenya`
