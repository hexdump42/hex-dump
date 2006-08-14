__doc__ = '''
Create an IronPython Windows application (No Console) executable from one 
or more python source files.

ipy.exe makeexe.py source1 [source2....] executable_name

For example:

 ipy.exe makeexe.py hello.py hello.exe

The first file in the source file argument list must contain the main logic.
'''
__version__ = "$Revision$"[11:-1]
import sys
from IronPython.Hosting import PythonCompiler
from System.Reflection.Emit import PEFileKinds

if sys.argv[1] == "--help":
    print __doc__
    sys.exit(0)

from System.Collections.Generic import List
sources = List[str]()

for file in sys.argv[1:-1]:
    sources.Add(file)
exename = sys.argv[-1]

compiler = PythonCompiler(sources, exename)
compiler.MainFile = sys.argv[1]
compiler.TargetKind = PEFileKinds.WindowApplication
compiler.IncludeDebugInformation = False 
compiler.Compile()
