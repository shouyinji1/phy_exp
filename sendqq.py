#!/usr/bin/python3
import os

def sendqq(send_file,qq,qq_type):
    #f=open('./main_file.sh','w+')
    #f.write('#!/bin/bash\n')
    #f.write('qq send '+qq_type+' ' +qq+' \"')
    #f.close()
    os.system('echo #!/bin/bash')
    os.system('echo qq send '+qq_type+' '+qq+' \\\" > main_file.sh')
    os.system('cat '+str(send_file)+ ' >> main_file.sh')
    os.system('echo \\\" >> main_file.sh')
    os.system('chmod +x main_file.sh')
    os.system('./main_file.sh')

