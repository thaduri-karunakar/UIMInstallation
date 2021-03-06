import sys
import time
import traceback
import windowsDataPopulationGlobalVariable as gfile
from pypsexec.client import Client

start = time.time()
netusecmd = r"net use \\{}\QA\NimBUS-install\Probes\SystemTestingProbes {} /user:{}\{}".format(gfile.fileShareIP,
    gfile.fileSharePassword, gfile.hostName, gfile.fileShareUserName )


def remote_connection():
    try:
        global c
        c = None
        c = Client(gfile.uimServer, gfile.uimServerLoginName, gfile.uimServerLoginPassword, encrypt='False')
        c.connect()
        c.create_service()

        # return c
    except Exception as e:
        print('Below exception occured .....\n')
        traceback.print_exc()
        print("Exit from the program with above issue...")
        sys.exit(1)
    else:

        print('service created for following "{}".......\n\n'.format(gfile.uimServer))


def archive_pkg_copying():
    """ copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""
    try:
        # remote_connection().create_service()

        print("copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine")
        stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(netusecmd))
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        print(netusecmd)
        if rc == 0:
            print('net use command executed successfully : ', stdout)
            archive_pkg_copy_cmd = r"echo All | copy \\{}\qa\NimBUS-install\Probes\SystemTestingProbes\{}\*.zip {}\archive".format(gfile.fileShareIP, gfile.uimVersion, gfile.uimPath)
            stdout1, stderr1, rc1 = c.run_executable("cmd.exe", arguments='''/c  {} '''.format(archive_pkg_copy_cmd))
            stdout1 = str(stdout1, 'utf-8')
            stderr1 = str(stderr1, 'utf-8')
            if rc1 == 0:
                print('archive_pkg_copy_cmd command executed successfully...')
                stdout2, stderr2, rc2 = c.run_executable('cmd.exe', arguments=''' /c {} '''.format(gfile.probe_deactivate))
                stdout2 = str(stdout2, 'utf-8')
                stderr2 = str(stderr2, 'utf-8')
                time.sleep(2)
                if rc2 == 0:
                    if ("_command failed: communication error" not in stdout2) or ("command not found" not in stdout2):
                        print('ade_deactivate command executed successfully...')
                        time.sleep(5)
                        stdout3, stderr3, rc3 = c.run_executable('cmd.exe', arguments=''' /c {} '''.format(gfile.probe_activate))
                        stdout3 = str(stdout3, 'utf-8')
                        stderr3 = str(stderr3, 'utf-8')
                        if rc3 == 0:
                            if ("_command failed: communication error" not in stdout3) or ("command not found" not in stdout3):
                                print('ade_activate command executed successfully...')
                                time.sleep(10)
                            else:
                                print('Failed to execute ade_activate command : ', stderr3)
                                remote_connection_close()
                                print("Exit from the program with above issue...")
                                sys.exit()

                    else:
                        print('Failed to execute ade_deactivate command : ', stderr2)
                        remote_connection_close()
                        print("Exit from the program with above issue...")
                        sys.exit()
                else:
                    print('Failed to execute ade_deactivate command : ', stderr2)
                    remote_connection_close()
                    print("Exit from the program with above issue...")
                    sys.exit()

            else:
                print('Failed to execute archive_pkg_copy_cmd command  :  {}\n{} '.format(stderr1, archive_pkg_copy_cmd))
                remote_connection_close()
                print("Exit from the program with above issue...")
                sys.exit()

        else:
            print('Failed to execute net use command :  {}.......\n {} '.format(stderr, stdout))
            remote_connection_close()
            print("Exit from the program with above issue...")
            sys.exit()

    except Exception as e:
        print('Below exception occured')
        traceback.print_exc()


def probe_deplyment():
    """ Deploying probes on primary robot of uim server """
    try:
        # c.create_service()
        print("Deploying probes on primary robot of uim server")
        for probe in ('cdm', 'dirscan', 'logmon', 'processes', 'net_connect'):
            probe_deploy = gfile.probe_deploy
            probe_deployment = probe_deploy.replace("probename", probe)
            print(probe_deployment)
            stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(probe_deployment))
            stdout = str(stdout, 'utf-8')
            stderr = str(stderr, 'utf-8')
            if rc == 0:
                if ("_command failed: communication error" not in stdout) or ("command not found" not in stdout):
                    print('{} probe deployed successfully:  \n {} \n'.format(probe, stdout), '*' * 43, sep='')
                    time.sleep(2)
            else:
                print('Failed to deploy {} probe :   {}\n {} '.format(probe, stdout, rc))
                remote_connection_close()
                print("Exit from the program with above issue...")
                sys.exit()
        print("waiting for 30 sec to finish probe deployment\n", '*' * 43, sep='')
        time.sleep(30)
    except Exception as e:
        print('Below exception occured .....\n')
        traceback.print_exc()

def cfg_replacing():
    """ copying/replacing  cfg files from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""

    try:
        # c.create_service()
        print("waiting for 30 sec to finish probe deactivation\n", '*' * 43, sep='')
        time.sleep(30)
        print(r"copying/replacing  cfg files from LVFILESHARE.dhcp.broadcom.net to UIM server machin\\n", '*' * 43, sep='')
        cdmcfg = r"echo All | copy \\{}\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\cdm.cfg {}\probes\system\cdm".format(gfile.fileShareIP, gfile.uimVersion, gfile.uimPath)
        stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(netusecmd))
        stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(cdmcfg))
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        if rc == 0:
            print('CDM cfg file replaced successfully...')
            dirscancfg = r"echo All | copy \\{}\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\dirscan.cfg {}\probes\system\dirscan".format(gfile.fileShareIP, gfile.uimVersion, gfile.uimPath)
            stdout1, stderr1, rc1 = c.run_executable("cmd.exe",
                                                                       arguments='''/c  {} '''.format(dirscancfg))
            stdout1 = str(stdout1, 'utf-8')
            stderr1 = str(stderr1, 'utf-8')
            if rc1 == 0:
                print('dirscan cfg file replaced successfully...')
                logmoncfg = r"echo All | copy \\{}\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\logmon.cfg {}\probes\system\logmon".format(gfile.fileShareIP, gfile.uimVersion, gfile.uimPath)
                stdout2, stderr2, rc2 = c.run_executable('cmd.exe',
                                                                           arguments=''' /c {} '''.format(logmoncfg))
                stdout2 = str(stdout2, 'utf-8')
                stderr2 = str(stderr2, 'utf-8')
                if rc2 == 0:
                    print('logmon cfg file replaced successfully...')
                    processescfg = r"echo All | copy \\{}\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\processes.cfg {}\probes\system\processes".format(gfile.fileShareIP, gfile.uimVersion, gfile.uimPath)
                    stdout3, stderr3, rc3 = c.run_executable('cmd.exe',
                                                                               arguments=''' /c {} '''.format(
                                                                                   processescfg))
                    stdout3 = str(stdout3, 'utf-8')
                    stderr3 = str(stderr3, 'utf-8')
                    if rc3 == 0:
                        print('processes cfg file replaced successfully...')
                        net_connectcfg = r"echo All | copy \\{}\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\network\net_connect.cfg {}\probes\network\net_connect".format(gfile.fileShareIP, gfile.uimVersion, gfile.uimPath)
                        stdout4, stderr4, rc4 = c.run_executable('cmd.exe',
                                                                                   arguments=''' /c {} '''.format(
                                                                                       net_connectcfg))
                        stdout4 = str(stdout4, 'utf-8')
                        stderr4 = str(stderr4, 'utf-8')
                        if rc4 == 0:
                            print('net_connect cfg file replaced successfully...')
                            # sleeping 5 sec for cfg replacing
                            time.sleep(5)

                        else:
                            print("Failed to replace net_connect cfg file :  {}\n{} ".format(stderr4, net_connectcfg))
                            remote_connection_close()
                            print("Exit from the program with above issue...")
                            sys.exit()

                    else:
                        print("Failed to replace processes cfg file  :  {}\n{} ".format(stderr3, processescfg))
                        remote_connection_close()
                        print("Exit from the program with above issue...")
                        sys.exit()

                else:
                    print('Failed to replace logmon cfg file  : {}\n{} '.format(stderr2, dirscancfg))
                    remote_connection_close()
                    print("Exit from the program with above issue...")
                    sys.exit()

            else:
                print('Failed to replace dirscan cfg file   :  {}\n{} '.format(stderr1, dirscancfg))
                remote_connection_close()
                print("Exit from the program with above issue...")
                sys.exit()

        else:
            print('Failed to replace cdm cfg file :  {}\n {} '.format(stderr, stdout))
            remote_connection_close()
            print("Exit from the program with above issue...")
            sys.exit()

    except Exception as e:
        print('Below exception occured .....\n')
        traceback.print_exc()


def probe_restart(probe_status):
    """ Restarting probes on primary robot of uim server """
    try:
        print("{} on primary robot of uim server\n".format(probe_status), '*' * 43, sep='')
        for probe in ['cdm', 'dirscan', 'logmon', 'processes', 'net_connect']:
            probe_status_change = gfile.probe_status
            probe_status_change = probe_status_change.replace("automated_deployment_engine", probe)
            probe_status_change = probe_status_change.replace("probe_status", probe_status)
            stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(probe_status_change))
            stdout = str(stdout, 'utf-8')
            stderr = str(stderr, 'utf-8')
            if rc == 0:
                if ("_command failed: communication error" in stdout) or ("command not found" in stdout):
                    print('{} failed for probe :  {}\n{}\n'.format(probe_status, probe, stdout), '*' * 43, sep='')
                    remote_connection_close()
                    print("Exit from the program with above issue...")
                    sys.exit()

                else:
                    print('{}d successfully: {} \n'.format(probe_status, probe), '*' * 43, sep='')
                    print(stdout, '\n')
                    time.sleep(5)
            else:
                print('{} failed for probe :  {}\n {}\n'.format(probe_status, probe, stderr), '*' * 43, sep='')
                remote_connection_close()
                print("Exit from the program with above issue...")
                sys.exit()
    except Exception as e:
        print('Below exception occured')
        traceback.print_exc()

def remote_connection_close():
    if c is not None:
        c.remove_service()
        c.disconnect()
        print('service removed for following "{}"'.format(gfile.uimServer))
        print('Script has taken', (time.time() - start) / 60, 'Minuets..')


remote_connection()
archive_pkg_copying()
probe_deplyment()
probe_restart('probe_deactivate')
cfg_replacing()
probe_restart('probe_activate')
remote_connection_close()
