import sys
from queuedirectory import QueueDir

qd = QueueDir("/tmp/jq")
entry = qd.new_entry()
cmdfile = open(sys.argv[1])
entry.writelines(cmdfile.readlines())
entry.commit()
cmdfile.close()
