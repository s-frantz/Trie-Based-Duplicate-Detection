def GetDuplicates_v2(
    inputLYR,
    fields=['SHAPE@'],
    where_clause="#",
    delete=False,
    ):

    def truncateCoordinates(myGeometry):
        # Needed as per https://gis.stackexchange.com/questions/40481/comparing-two-geometries-in-arcpy
        # because of ESRI bugs related to storing shape data in float format:
            # https://en.wikipedia.org/wiki/Floating-point_arithmetic#Accuracy_problems
        truncated_coords = []
        partnum = -1
        for part in (myGeometry):
            partnum += 1
            try:
                for pnt in myGeometry.getPart(partnum):
                    if pnt:
                        truncated_coords.append("{:10.6f}".format(pnt.X))
                        truncated_coords.append("{:10.6f}".format(pnt.Y))
            except TypeError: # point geometry
                truncated_coords.append("{:10.6f}".format(part.X))
                truncated_coords.append("{:10.6f}".format(part.Y))
        return truncated_coords


    import arcpy, sys
    sys.path.append(r'\\ace-ra-fs1\data\GIS\_Dev\python\apyx')
    from apyx import Update, DuplicationTrie

    arcpy.AddMessage("\n{} will be tested for duplicates; 'OBJECTID' will be used as unique identifier.\n".format(fields))

    T = DuplicationTrie()

    with arcpy.da.SearchCursor(inputLYR, fields + ['OID@'], where_clause=where_clause) as sCur:
        for row in sCur:

            if 'SHAPE@' in fields:
                row[fields.index('SHAPE@')] = truncateCoordinates(row[fields.index('SHAPE@')])

            rowString = ";".join([str(row[i]) for i in range(len(fields))])
            oid = row[-1]

            T.Store(rowString, oid)

    redundant_oids = [oid for redundancy, oids in T.Report().items() for oid in oids[1:]]
    redundant_terms = [k for k in T.Report().keys()]

    if not delete:
        arcpy.AddMessage("The following lists are for reporting purposes only.")

    arcpy.AddMessage("Redundant OIDs (total of {}):\nOBJECTID In {}".format(
        len(redundant_oids), tuple(redundant_oids)
        )
    )

    if 'SHAPE@' not in fields:
        arcpy.AddMessage("Redundant terms (" + str(fields) + "):")
        arcpy.AddMessage(" ")
        set_redundant_terms = set(redundant_terms)
        for rt in list(set_redundant_terms):
            arcpy.AddMessage("    " + str(rt))
        arcpy.AddMessage(" ")

    if delete and len(redundant_oids) > 0:
        def deleteSelectOids():
            if len(redundant_oids) > 1:
                query = "OBJECTID In " + str(tuple(redundant_oids))
            else:
                query = "OBJECTID = " + str(redundant_oids[0])
            with arcpy.da.UpdateCursor(inputLYR, ['OBJECTID'], query) as uCur:
                for row in uCur:
                    uCur.deleteRow()
            arcpy.AddMessage("Deleted above, and kept the following OBJECTIDs:\n{}\n".format(unique_oids))

        desc = arcpy.Describe(inputLYR)
        if ".sde" in desc.catalogPath:
            sdePath = desc.catalogPath.split('.sde')[0]+".sde"
            Update(sdePath, deleteSelectOids)
        else:
            deleteSelectOids()