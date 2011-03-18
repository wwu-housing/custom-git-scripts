import os
import subprocess

# can be either the CVSROOT or the location of a copy
CVS_ROOT = "/usr/home/user/cvs_copy/"
GIT_HOST = "git@test.edu"

directories = {
    "EXPORT_DIR": "/usr/home/user/modules/",
    "GIT": "/usr/home/user/repositories/",
}

for directory in directories.values():
    if not os.path.isdir(directory):
        # recursively make the directories, if they don't exist
        os.makedirs(directory)

# a list of all the modules in the CVS_ROOT, excluding the CVSROOT folder
modules = [directory for directory in os.listdir(CVS_ROOT) if os.path.isdir(os.path.join(CVS_ROOT, directory)) and not directory == "CVSROOT"]

for module in modules:
    print "+- Started %s module" % module

    # create a git repository from a cvs module
    command = "sudo git cvsimport -a -i -k -d %s -C %s.git %s" % (
        CVS_ROOT,
        os.path.join(directories["EXPORT_DIR"], module),
        module)
    subprocess.call(command, shell=True)

    if not os.path.isdir("%s.git" % os.path.join(directories["EXPORT_DIR"], module)):
        raise Exception("git cvs import failed on %s module" % module)
    print "|- git cvs import success on %s module" % module

    # checkout a copy of the module from the local git repository created above
    command = "git clone -l %s.git %s" % (
        os.path.join(directories["EXPORT_DIR"], module),
        os.path.join(directories["GIT"], module))
    subprocess.call(command, shell=True)

    if not os.path.isdir(os.path.join(directories["GIT"], module)):
        raise Exception("local git clone failed on %s module" % module)
    print "|- local git clone success on %s module" % module

    # push the checkout copy from above to the remote repository
    os.chdir(os.path.join(directories["GIT"], module))
    command = "git push --mirror %s:%s.git" % (GIT_HOST, module)
    subprocess.call(command, shell=True)

    print "-- Completed %s module" % module

