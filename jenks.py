import arcpy, pysal, numpy, scipy
print "Importing packages..."
#The arcpy package, of course, is the Python package for ArcGIS functions.  The
#  pysal package is an open-source package of geography functions that is not
#  included in ArcGIS, but can be downloaded free on the internet.  The numpy
#  package is included in more recent distributions of Python, and contains the
#  numeric array processing functions necessary to speed up calculations for
#  large arrays.

print "Importing functions..."
from pysal.esda.mapclassify import Natural_Breaks as nb
#The Jenks Natural Breaks function is contained in the pysal package under the
#  name pysal.esda.mapclassify.Natural_Breaks.  For simplicity's sake we will
#  rename this formula as nb for later use in the code.

print "Converting IQHO to Numpy Array..."
fc = "IQH_Temp_join3.shp"
field = "IQHO"
myArray = arcpy.da.FeatureClassToNumPyArray(fc, field, skip_nulls=True)
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
arcpy.AddField_management(fc, newfield, "SHORT")
arcpy.da.NumPyArrayToFeatureClass(breaks,fc,newfield)
#The new field, called "Jenks", is added to the table in the specified fc parameter
#  from before as a short integer (as the field will contain numbers representing Jenks
#  categories, and as such will always be integers and will be small enough that the
#  long format for integers will likely not be required.
#The breaks array calculated before is then transferred into this new "Jenks" field.
