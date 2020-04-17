import sys
import time
import dataPopulationGlobalVariable as gfile
from pypsexec.client import Client

start = time.time()
netusecmd = r"net use \\10.17.172.178\QA\NimBUS-install\Probes\SystemTestingProbes interOP@123 /user:w19server1\administrator"


def archive_pkg_copying():
    """ copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""
    try:
        global c
        c = Client(gfile.uimserver, gfile.username, gfile.password, encrypt='False')
        c.connect()

        c.create_service()
        # print('service created for following "{}".......\n\n'.format(gfile.uimserver))
        print("copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine")
        netusecmd = r"net use \\10.17.172.178\QA\NimBUS-install\Probes\SystemTestingProbes interOP@123 /user:w19server1\administrator"
        stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(netusecmd))
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        if rc == 0:
            print('net use command executed successfully : ', stdout)
            archive_pkg_copy_cmd = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\{}\*.zip C:\PROGRA~1\Nimsoft\archive".format(
                gfile.uimversion)
            stdout1, stderr1, rc1 = c.run_executable("cmd.exe", arguments='''/c  {} '''.format(archive_pkg_copy_cmd))
            stdout1 = str(stdout1, 'utf-8')
            stderr1 = str(stderr1, 'utf-8')
            if rc1 == 0:
                print('archive_pkg_copy_cmd command executed successfully...')
                stdout2, stderr2, rc2 = c.run_executable('cmd.exe',
                                                         arguments=''' /c {} '''.format(gfile.probe_deactivate))
                stdout2 = str(stdout2, 'utf-8')
                stderr2 = str(stderr2, 'utf-8')
                if rc2 == 0:
                    print('ade_deactivate command executed successfully...')
                    time.sleep(5)
                    stdout3, stderr3, rc3 = c.run_executable('cmd.exe',
                                                             arguments=''' /c {} '''.format(gfile.probe_activate))
                    stdout3 = str(stdout3, 'utf-8')
                    stderr3 = str(stderr3, 'utf-8')
                    if rc3 == 0:
                        print('ade_activate command executed successfully...')
                        time.sleep(5)
                    else:
                        print('Failed to execute ade_activate command : ', stderr3)

                else:
                    print('Failed to execute ade_deactivate command : ', stderr2)

            else:
                print(
                    'Failed to execute archive_pkg_copy_cmd command  :  {}\n{} '.format(stderr1, archive_pkg_copy_cmd))

        else:
            print('Failed to execute net use command :  {}.......\n {} '.format(stderr, stdout))
            sys.exit()

    except Exception as e:
        print('Below exception occured')
        print(e)
        print()
    finally:
        c.remove_service()
        c.disconnect()
        # print('Connection closed for following host {}'.format(gfile.uimserver))


def cfg_replacing():
    """ copying/replacing  cfg files from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""

    try:
        c = Client(gfile.uimserver, gfile.username, gfile.password, encrypt='False')
        c.connect()

        c.create_service()
        print("waiting for 30 sec to finish probe deployment....")
        time.sleep(30)
        print(r"copying/replacing  cfg files from LVFILESHARE.dhcp.broadcom.net to UIM server machin")
        cdmcfg = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\cdm.cfg C:\PROGRA~1\Nimsoft\probes\system\cdm".format(gfile.uimversion)
        stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(netusecmd))
        stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(cdmcfg))
        stdout = str(stdout, 'utf-8')
        stderr = str(stderr, 'utf-8')
        if rc == 0:
            print('CDM cfg file replaced successfully...')
            dirscancfg = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\dirscan.cfg C:\PROGRA~1\Nimsoft\probes\system\dirscan".format(gfile.uimversion)
            stdout1, stderr1, rc1 = c.run_executable("cmd.exe", arguments='''/c  {} '''.format(dirscancfg))
            stdout1 = str(stdout1, 'utf-8')
            stderr1 = str(stderr1, 'utf-8')
            if rc1 == 0:
                print('dirscan cfg file replaced successfully...')
                logmoncfg = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\logmon.cfg C:\PROGRA~1\Nimsoft\probes\system\logmon".format(gfile.uimversion)
                stdout2, stderr2, rc2 = c.run_executable('cmd.exe', arguments=''' /c {} '''.format(logmoncfg))
                stdout2 = str(stdout2, 'utf-8')
                stderr2 = str(stderr2, 'utf-8')
                if rc2 == 0:
                    print('logmon cfg file replaced successfully...')
                    processescfg = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\system\processes.cfg C:\PROGRA~1\Nimsoft\probes\system\processes".format(gfile.uimversion)
                    stdout3, stderr3, rc3 = c.run_executable('cmd.exe', arguments=''' /c {} '''.format(processescfg))
                    stdout3 = str(stdout3, 'utf-8')
                    stderr3 = str(stderr3, 'utf-8')
                    if rc3 == 0:
                        print('processes cfg file replaced successfully...')
                        net_connectcfg = r"echo All | copy \\10.17.172.178\qa\NimBUS-install\Probes\SystemTestingProbes\{}\Windows_CFG\network\net_connect.cfg C:\PROGRA~1\Nimsoft\probes\network\net_connect".format(
                            gfile.uimversion)
                        stdout4, stderr4, rc4 = c.run_executable('cmd.exe',
                                                                 arguments=''' /c {} '''.format(net_connectcfg))
                        stdout4 = str(stdout4, 'utf-8')
                        stderr4 = str(stderr4, 'utf-8')
                        if rc4 == 0:
                            print('net_connect cfg file replaced successfully...')
                        else:
                            print("Failed to replace net_connect cfg file :  {}\n{} ".format(stderr4, net_connectcfg))

                    else:
                        print("Failed to replace processes cfg file  :  {}\n{} ".format(stderr3, processescfg))

                else:
                    print('Failed to replace logmon cfg file  : {}\n{} '.format(stderr2, dirscancfg))

            else:
                print('Failed to replace dirscan cfg file   :  {}\n{} '.format(stderr1, dirscancfg))

        else:
            print('Failed to replace cdm cfg file :  {}\n {} '.format(stderr, stdout))

    except Exception as e:
        print('Below exception occured .....\n')
        type, value, traceback = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        print()
    finally:
        c.remove_service()
        c.disconnect()
        # print('Connection closed for following host {}'.format(gfile.uimserver))


def probe_deplyment():
    """ Deploying probes on primary robot of uim server """
    try:
        c = Client(gfile.uimserver, gfile.username, gfile.password, encrypt='False')
        c.connect()

        c.create_service()
        print("Deploying probes on primary robot of uim server")
        for probe in ('cdm', 'dirscan', 'logmon', 'processes', 'net_connect'):
            probe_deploy = gfile.probe_deploy
            probe_deployment = probe_deploy.replace("probename", probe)
            stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(probe_deployment))
            stdout = str(stdout, 'utf-8')
            stderr = str(stderr, 'utf-8')
            if rc == 0:
                print('{} probe deployed successfully...'.format(probe))
                time.sleep(2)
            else:
                print('Failed to deploy {} probe :   {} '.format(probe, stderr))

    except Exception as e:
        print('Below exception occured .....\n')
        type, value, traceback = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        # print(e)
        print()
    finally:
        c.remove_service()
        c.disconnect()
        # print('Connection closed for following host {}'.format(gfile.uimserver))


def probe_restart():
    """ Restarting probes on primary robot of uim server """
    try:
        c = Client(gfile.uimserver, gfile.username, gfile.password, encrypt='False')
        c.connect()

        c.create_service()

        print("Restarting probes on primary robot of uim server")
        for probe in ['cdm', 'dirscan', 'logmon', 'processes', 'net_connect']:
            probe_deactivate = gfile.probe_deactivate
            probe_deactivate = probe_deactivate.replace("automated_deployment_engine", probe)
            stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(probe_deactivate))
            stdout = str(stdout, 'utf-8')
            stderr = str(stderr, 'utf-8')
            if rc == 0:
                print('{} probe deactivated successfully...'.format(probe))
                time.sleep(5)
                probe_activate = gfile.probe_activate
                probe_activate = probe_activate.replace("automated_deployment_engine", probe)
                stdout, stderr, rc = c.run_executable("cmd.exe", arguments='''/c  {}'''.format(probe_activate))
                stdout = str(stdout, 'utf-8')
                stderr = str(stderr, 'utf-8')
                if rc == 0:
                    print('{} probe activated successfully...'.format(probe))
                    time.sleep(2)
                else:
                    print('Failed to activate {} probe :  {}\n {} '.format(probe, stderr))


            else:
                print('Failed to deactivate {} probe :  {}\n {} '.format(probe, stderr))

    except Exception as e:
        print('Below exception occured')
        print(e)
        print()
    finally:
        c.remove_service()
        c.disconnect()
        # print('Connection closed for following host {}'.format(gfile.uimserver))


archive_pkg_copying()
probe_deplyment()
cfg_replacing()
probe_restart()
