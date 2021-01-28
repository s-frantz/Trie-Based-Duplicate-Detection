# Trie-Based-Duplicate-Detection
Accepts an arbitrary combinations of fields (including geometry) and returns duplicate records.

The recently coded trie class 'DuplicationTrie.py' is called from within a fork of an older function (GetDuplicates_v2). The prior version of this tool ran with time complexity of O(n^2), fine for most feature classes, but we found the need for a better performing tool with certain larger datasets, or with comparing polygon geometries (arrays of coordinates).

Based on theory and testing, i.e. in "SearchAlgoPerformance.png", the Trie-based variation is much closer to linear time and space efficiency.

The tool can be run from an Arc10.X toolbox using the following __main__ logic and validation code. Parameters / layout are in the "GUI.png"

# __main__.py

import arcpy, sys
sys.path.append(r"\\ace-ra-fs1\data\GIS\_Dev\python\apyx")
from apyx import GetDuplicates_v2

GetDuplicates_v2(   inputLYR = arcpy.GetParameter(0),
                    fields = arcpy.GetParameterAsText(1).split(";"),
                    delete = arcpy.GetParameter(2),
                    )

# __validation__

import arcpy
class ToolValidator(object):
  """Class for validating a tool's parameter values and controlling
  the behavior of the tool's dialog."""

  def __init__(self):
    """Setup arcpy and the list of tool parameters."""
    self.params = arcpy.GetParameterInfo()

  def initializeParameters(self):
    """Refine the properties of a tool's parameters.  This method is
    called when the tool is opened."""
    return

  def updateParameters(self):
    """Modify the values and properties of parameters before internal
    validation is performed.  This method is called whenever a parameter
    has been changed."""
    if self.params[0].value is not None:
      list_of_str_fields = [
	      str(f.name) for f in arcpy.ListFields(self.params[0].value)
	      if str(f.name) not in ('SHAPE', 'OBJECTID')
	    ]
	    self.params[1].filter.list = ['SHAPE@'] + list_of_str_fields
    return

  def updateMessages(self):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return

