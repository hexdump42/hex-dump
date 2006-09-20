import clr
clr.AddReference("libgphoto2-sharp.dll")
import LibGPhoto2

# Setup and detect cameras
cx = LibGPhoto2.Context()
abilities_list = LibGPhoto2.CameraAbilitiesList()
abilities_list.Load(cx)
camera_list = LibGPhoto2.CameraList()
port_info_list = LibGPhoto2.PortInfoList()
port_info_list.Load()
abilities_list.Detect(port_info_list, camera_list, cx)
print "Found %s camera(s)" % camera_list.Count()

# Select camera on port
camera_model = camera_list.GetName(0)
print "Selecting camera %s" % camera_model
camera_index = abilities_list.LookupModel(camera_model)
camera_abilities = abilities_list.GetAbilities(camera_index)
camera = LibGPhoto2.Camera()
camera.SetAbilities(camera_abilities)
path = camera_list.GetValue(0)
print "gphoto path %s" % path
camera_port_info_list_index = port_info_list.LookupPath(path)
port_info = port_info_list.GetInfo(camera_port_info_list_index)
camera.SetPortInfo(port_info)

# Init camera
camera.Init(cx)
camera_fs = camera.GetFS()

files = []

def get_filelist(dir):
    filelist = camera_fs.ListFiles(dir,cx)
    i = 0
    while i < filelist.Count():
        files.append((dir,filelist.GetName(i)))
        i += 1
    # process subdirectories
    folderlist = camera_fs.ListFolders(dir, cx)
    i = 0
    while i < folderlist.Count():
        get_filelist(dir + folderlist.GetName(i) + "/")
        i += 1

get_filelist("/")
print files
    



