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
