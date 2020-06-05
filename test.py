import sys
import time
import windowsDataPopulationGlobalVariable as gfile
from pypsexec.client import Client

start = time.time()


def remote_connection():
    try:
        c = Client(gfile.uimserver, gfile.username, gfile.password, encrypt='False')
        c.connect()
        return c
    except Exception as e:
        print('Below exception occured while connecting with .....{}\n'.format(gfile.uimserver))
        print(e)
        print()


def archive_pkg_copying():
    """ copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""
    try:
        print('service created for following "{}".......\n\n'.format(gfile.uimserver))
        remote_connection().create_service()
        netusecmd = r"net use \\10.17.172.178\QA\NimBUS-install\Probes\SystemTestingProbes interOP@123 /user:w19server1\administrator"
        print(netusecmd)
        stdout, stderr, rc = remote_connection().run_executable("cmd.exe", arguments='''/c  {}'''.format(netusecmd))
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        if rc == 0:
            print('net use command executed successfully : ', stdout)
            archive_pkg_copy_cmd = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\201\*.zip C:\PROGRA~1\Nimsoft\archive"
            print(archive_pkg_copy_cmd)
            remote_connection().create_service()
            stdout1, stderr1, rc1 = remote_connection().run_executable("cmd.exe", arguments='''/c  {} '''.format(archive_pkg_copy_cmd))
            stdout1 = str(stdout1, 'utf-8')
            stderr1 = str(stderr1, 'utf-8')
            if rc1 == 0:
                print('archive_pkg_copy_cmd command executed successfully : ', stdout1)
                stdout2, stderr2, rc2 = remote_connection().run_executable('cmd.exe',
                                                                           arguments=''' /c {} '''.format(
                                                                               gfile.ade_deactivate))
                stdout2 = str(stdout2, 'utf-8')
                stderr2 = str(stderr2, 'utf-8')
                if rc2 == 0:
                    print('ade_deactivate command executed successfully : ', stdout2)
                    time.sleep(5)
                    stdout3, stderr3, rc3 = remote_connection().run_executable('cmd.exe',
                                                                               arguments=''' /c {} '''.format(
                                                                                   gfile.ade_activate))
                    stdout3 = str(stdout3, 'utf-8')
                    stderr3 = str(stderr3, 'utf-8')
                    if rc3 == 0:
                        print('ade_activate command executed successfully : ', stdout3)
                        time.sleep(5)
                    else:
                        print('Failed to execute ade_activate command : ', stderr3)

                else:
                    print('Failed to execute ade_deactivate command : ', stderr2)

            else:
                print('Failed to execute archive_pkg_copy_cmd command  :  {}\n{} '.format(stderr1, archive_pkg_copy_cmd))

        else:
            print('Failed to execute net use command :  {}.......\n {} '.format(stderr, stdout))
            sys.exit()

    except Exception as e:
        print('Below exception occured')
        print(e)
        print()


def cfg_replacing():
    """ copying/replacing  cfg files from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""

    stdout, stderr, rc = remote_connection().run_executable('cmd.exe', arguments=''' /c ipconfig ''')
    print(stdout)


def remote_connection_close():
    remote_connection().remove_service()
    remote_connection().disconnect()
    print('service removed for following "{}"'.format(gfile.uimserver))
    print('Script has taken', (time.time() - start) / 60, 'Minuets..')


remote_connection()
archive_pkg_copying()
# cfg_replacing()
remote_connection_close()
