import time
import paramiko
import traceback
import linuxDataPopulationGlobalVariable as gfile
import sys

start = time.time()


def remote_connection():
    try:
        ssh = paramiko.SSHClient()  # Creating Connection
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(gfile.uimserver, gfile.port, gfile.vm_username, gfile.vm_password)
        return ssh
    except Exception as e:
        print('Below exception occured .....\n')
        type, value, traceback = sys.exc_info()
        print('Error opening %s: %s' % (value.filename, value.strerror))
        print()


def archive_pkg_copying():
    """ copying packages from /mnt/fileshare location to UIM server Archive"""

    try:
        # ssh = paramiko.SSHClient()  # Creating Connection
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(gfile.uimserver, gfile.port, gfile.vm_username, gfile.vm_password)
        print('service created for following {}\n'.format(gfile.uimserver), '*' * 43, sep='')
        print('copying packages from /mnt/fileshare location to UIM server Archive\n', '*' * 68, sep='')
        ''' Finding the fileshare path '''
        global filesharepath
        filesharepath = """ find /mnt/fileshare/ -type d -name "SystemTestingProbes" """
        stdin, stdout, stderr = remote_connection().exec_command(filesharepath)
        time.sleep(5)
        stdout = ''.join(stdout);
        filesharepath = stdout.strip()
        print('Fileshare path is : \n {}\n'.format(filesharepath), '=' * 50, sep='')
        packages = '\cp {}/{}/*.zip /opt/nimsoft/archive'.format(filesharepath, gfile.uimversion)
        # print(packages)
        stdin, stdout, stderr = remote_connection().exec_command(packages)
        time.sleep(5)
        stdout = ''.join(stdout);
        stdout = stdout.strip()
        stderr = ''.join(stderr);
        stderr = stderr.strip()

        if len(stderr) == 0:
            print("copying packages from /mnt/fileshare location to UIM server Archive has successfully\n", '*' * 70,
                  sep='')
            probe_deactive_stdin, probe_deactive_stdout, probe_deactive_stderr = remote_connection().exec_command(
                gfile.probe_deactivate)
            probe_deactive_stdout = ''.join(probe_deactive_stdout);
            probe_deactive_stdout = probe_deactive_stdout.strip()
            probe_deactive_stderr = ''.join(probe_deactive_stderr);
            probe_deactive_stderr = probe_deactive_stderr.strip()
            if len(probe_deactive_stderr) == 0:
                print("ade_deactivate command executed successfully \n", '*' * 43, sep='')
                time.sleep(5)
                probe_active_stdin, probe_active_stdout, probe_active_stderr = remote_connection().exec_command(
                    gfile.probe_activate)
                probe_active_stdout = ''.join(probe_active_stdout);
                probe_active_stdout = probe_active_stdout.strip()
                probe_active_stderr = ''.join(probe_active_stderr);
                probe_active_stderr = probe_active_stderr.strip()

                if len(probe_active_stderr) == 0:
                    print("ade_activate command executed successfully \n", '*' * 43, sep='')
                    print("ade is activating... sleeping for 5 sec....\n", '*' * 43, sep='')
                    time.sleep(5)

                else:
                    print("Failed to ade_activate command ....\n {}".format(probe_active_stderr), '*' * 43, sep='')
            else:
                print("Failed to ade_deactivate command....\n {}".format(probe_deactive_stderr), '*' * 43, sep='')
        else:
            print(
                "Failed to copying packages from /mnt/fileshare location to UIM server Archive \n {} \n".format(stderr),
                '*' * 100, sep='')

    except Exception as ex:
        traceback.print_exc()


def probe_deplyment():
    """ Deploying probes from archive to UIM server primary robot"""
    try:
        print("Deploying probes on primary robot of uim server....\n", '*' * 43, sep='')
        for probe in ('cdm', 'dirscan', 'logmon', 'processes', 'net_connect'):
            probe_deploy = gfile.probe_deploy
            probe_deploy = probe_deploy.replace("probename", probe)
            stdin, stdout, stderr = remote_connection().exec_command(probe_deploy)
            stdout = ''.join(stdout);
            stdout = stdout.strip()
            stderr = ''.join(stderr);
            stderr = stderr.strip()
            if len(stderr) == 0:
                print('{} probe deployed successfully \n'.format(probe), '*' * 43, sep='')
                time.sleep(5)
            else:
                print('Failed to deploy {} probe :   {}\n'.format(probe, stderr), '*' * 43, sep='')

    except Exception as e:
        traceback.print_exc()


def cfg_replacing():
    """ copying/replacing  cfg files from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""

    try:
        print("waiting for 30 sec to finish probe deployment\n", '*' * 43, sep='')
        time.sleep(30)
        print("copying/replacing  cfg files from /mnt/fileshare to UIM server machine \n", '*' * 43, sep='')
        cdmcfg = r"\cp {}/{}/Linux_CFG/system/cdm.cfg /opt/nimsoft/probes/system/cdm".format(filesharepath,
                                                                                             gfile.uimversion)
        stdin, stdout, stderr = remote_connection().exec_command(cdmcfg)
        stdout = ''.join(stdout);
        stdout = stdout.strip()
        stderr = ''.join(stderr);
        stderr = stderr.strip()
        if len(stderr) == 0:
            print('CDM cfg file replaced successfully \n', '*' * 43, sep='')
            dirscancfg = r"\cp {}/{}/Linux_CFG/system/dirscan.cfg /opt/nimsoft/probes/system/dirscan".format(filesharepath,
                gfile.uimversion)
            stdin, stdout, stderr = remote_connection().exec_command(dirscancfg)
            stdout = ''.join(stdout);
            stdout = stdout.strip()
            stderr = ''.join(stderr);
            stderr = stderr.strip()
            if len(stderr) == 0:
                print('dirscan cfg file replaced successfully \n', '*' * 43, sep='')
                logmoncfg = r"\cp {}/{}/Linux_CFG/system/logmon.cfg /opt/nimsoft/probes/system/logmon".format(filesharepath,
                    gfile.uimversion)
                stdin, stdout, stderr = remote_connection().exec_command(logmoncfg)
                stdout = ''.join(stdout);
                stdout = stdout.strip()
                stderr = ''.join(stderr);
                stderr = stderr.strip()
                if len(stderr) == 0:
                    print('logmon cfg file replaced successfully \n', '*' * 43, sep='')
                    processescfg = r"\cp {}/{}/Linux_CFG/system/processes.cfg /opt/nimsoft/probes/system/processes".format(filesharepath,
                        gfile.uimversion)
                    stdin, stdout, stderr = remote_connection().exec_command(processescfg)
                    stdout = ''.join(stdout);
                    stdout = stdout.strip()
                    stderr = ''.join(stderr);
                    stderr = stderr.strip()
                    if len(stderr) == 0:
                        print('processes cfg file replaced successfully \n', '*' * 43, sep='')
                        net_connectcfg = r"\cp {}/{}/Linux_CFG/network/net_connect.cfg /opt/nimsoft/probes/network/net_connect".format(filesharepath,
                            gfile.uimversion)
                        stdin, stdout, stderr = remote_connection().exec_command(net_connectcfg)
                        stdout = ''.join(stdout);
                        stdout = stdout.strip()
                        stderr = ''.join(stderr);
                        stderr = stderr.strip()
                        if len(stderr) == 0:
                            print('net_connect cfg file replaced successfully \n', '*' * 43, sep='')
                        else:
                            print("Failed to replace net_connect cfg file :  {}\n{}\n", '*' * 43,
                                  sep=''.format(stderr, net_connectcfg))

                    else:
                        print("Failed to replace processes cfg file  :  {}\n{}\n", '*' * 43,
                              sep=''.format(stderr, processescfg))

                else:
                    print('Failed to replace logmon cfg file  : {}\n{}\n', '*' * 43, sep=''.format(stderr, dirscancfg))

            else:
                print('Failed to replace dirscan cfg file   :  {}\n{}\n', '*' * 43, sep=''.format(stderr, dirscancfg))

        else:
            print('Failed to replace cdm cfg file :  {}\n {}\n', '*' * 43, sep=''.format(stderr, stdout))


    except Exception as ex:
        traceback.print_exc()
        print()


def probe_restart():
    """ Restarting probes on primary robot of uim server """
    try:
        print("Restarting probes on primary robot of uim server\n", '*' * 43, sep='')
        for probe in ['cdm', 'dirscan', 'logmon', 'processes', 'net_connect']:
            probe_deactivate = gfile.probe_deactivate
            probe_deactivate = probe_deactivate.replace("automated_deployment_engine", probe)
            stdin, stdout, stderr = remote_connection().exec_command(probe_deactivate)
            stdout = ''.join(stdout);
            stdout = stdout.strip()
            stderr = ''.join(stderr);
            stderr = stderr.strip()
            if len(stderr) == 0:
                print('{} probe deactivated successfully \n'.format(probe), '*' * 43, sep='')
                time.sleep(5)
                probe_activate = gfile.probe_activate
                probe_activate = probe_activate.replace("automated_deployment_engine", probe)
                stdin, stdout, stderr = remote_connection().exec_command(probe_activate)
                stdout = ''.join(stdout);
                stdout = stdout.strip()
                stderr = ''.join(stderr);
                stderr = stderr.strip()
                if len(stderr) == 0:
                    print('{} probe activated successfully \n'.format(probe), '*' * 43, sep='')
                    time.sleep(2)
                else:
                    print('Failed to activate probe :  {}\n {}\n'.format(probe, stderr), '*' * 43, sep='')
            else:
                print('Failed to deactivate probe :  {}\n {}\n'.format(probe, stderr), '*' * 43, sep='')


    except Exception as ex:

        traceback.print_exc()


def remote_connection_close():
    try:
        remote_connection().close()
        print('Connection closed for following host {} \n'.format(gfile.uimserver), '*' * 52, sep='')
        print('Script has taken', (time.time() - start) / 60, 'Minuets..')
    except Exception as ex:
        traceback.print_exc()


remote_connection()
archive_pkg_copying()
probe_deplyment()
cfg_replacing()
probe_restart()
remote_connection_close()
