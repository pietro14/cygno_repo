############# general TOOL for file #############

def mv_file(filein, fileout):
    import os
    command = '/bin/mv '+ filein +' '+ fileout
    return os.system(command)

def cp_file(filein, fileout):
    import os
    command = '/bin/cp '+ filein +' '+ fileout
    return os.system(command)

def rm_file(filein):
    import os
    command = '/bin/rm '+ filein
    return os.system(command)

def grep_file(what, filein):
    import subprocess
    command = '/usr/bin/grep ' + what +' '+filein
    status, output = subprocess.getstatusoutput(command)
    return output

def mkdir_file(folder):
    import os
    command = '/bin/mkdir -p '+ folder
    return os.system(command)


def append2file(line, filein):
    import os
    command = 'echo '+ line + ' >> '+filein
    return os.system(command)