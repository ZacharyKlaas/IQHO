import scipy, pandas, pysal
import arcpy
import numpy as np
import pandas as pd
from numpy import array
from pandas import DataFrame
print "Importing packages..."
#The arcpy package, of course, is the Python package for ArcGIS functions.  The
#  pysal package is an open-source package of geography functions that is not
#  included in ArcGIS, but can be downloaded free on the internet.  The numpy
#  package is included in more recent distributions of Python, and contains the
#  numeric array processing functions necessary to speed up calculations for
#  large arrays.  The scipy package contains scientific functions that are used
#  to power the functions provided by pysal.  The pandas package contains data
#  analysis functions used to power the functions provided by pysal.
#The numpy and pandas packages are instantiated because we will be using elements
#  of the array and DataFrame functions within those packages.

print "Importing functions..."
from pysal.esda.mapclassify import Natural_Breaks as nb
#The Jenks Natural Breaks function is contained in the pysal package under the
#  name pysal.esda.mapclassify.Natural_Breaks.  For simplicity's sake we will
#  instantiate this as nb for later use in the code.

print "Converting IQHO to Numpy Array..."
fc = "f:\\test\\IQH_Temp_join3.shp"
field = "IQH_Test"
myArray = arcpy.da.FeatureClassToNumPyArray(fc, field, skip_nulls=True)
myArray.dtype = np.float32
#The preceding calculation relies upon the arcpy.da (Data Analysis) and numpy packages.
#The fc parameter is the feature class upon which the operation is to be performed.
#The field parameter is the name of the field which is to be categorised into the
#  Jenks Natural Breaks categories.
#The "skip_nulls" flag allows null values to be rejected as a basis for the calculation
#  of the results, when equivalent to "True".  This can be edited out of the script
#  should it be desired to retain null values, but it should be remembered that null
#  values are distinct from values of zero, which generally one will want to retain
#  in calculations.  Null values typically represent "no data" for an area, and as
#  such, should be excluded from consideration by Jenks Natural Breaks calculations.
#Though the array is of integers, it is cast as a float because the PYSAL package
#  element KMEANS requires a float variable.  The results returning from PYSAL
#  are fed into integer fields, however.

print "Calculating breaks..."
breaks = nb(myArray.ravel(),k=4,initial=20)
#The preceding calculation relies upon the pysal package.
#The Natural_Breaks function only accepts a 1d vector of values; using numpy.ravel()
#  for this vector.
#The k parameter is the number of classes to be used by the Jenks function.
#The initial parameter is the "seed", which can be varied to speed up the calculation.
#(The tradeoff is speed versus consistency of calculation - since the Jenks function
#  is calculated by an iterative process, a fast calculation will not converge on the
#  best "answer" right away, though it will start to do so; a slow calculation, by
#  contrast, will be more likely to have converged on the best values, though at the
#  cost of slowness.  This is an important consideration if you're running this on
#  a big dataset.)

print "Checking for any previous calculations of the Jenks field..."
newfield = "Jenks"
try:
	arcpy.DeleteField_management(fc, newfield)
	print "Previous calculation of the Jenks field deleted..."

except Exception as e:
	print "No previous calculation of the Jenks field found..."
#If there was any field storing previous calculations for the Jenks Natural Breaks values,
#  this field is deleted, and then the next bit of code after this try-except block will
#  create this field anew.  If there is no such field, then the try block will throw an
#  exception rather than the program halting because no such field was found, and the
#  calculation of a Jenks Natural Breaks field can take place from scratch in the next
#  block of code.

print "Exporting results to feature class table..."
arcpy.AddField_management(fc,"index","long")
arcpy.AddField_management(fc,newfield,"long")
myData = pd.DataFrame(breaks.yb)
myData.columns = [newfield]
myReturnArray = myData.to_records()
arcpy.da.ExtendTable(fc, "FID", myReturnArray, "index", False)
arcpy.DeleteField_management(fc, "index")
#An index field is temporarily added, as the to_records() function appends the entire
#  array to the table, and the array we have produced contains an index field and
#  the new field with the natural breaks data.
#The new field, called "Jenks", is added to the table in the specified fc parameter
#  from before as a long integer (as the field will contain numbers representing Jenks
#  categories, and as such will always be integers.
#The breaks array calculated before is then transferred into this new "Jenks" field.
