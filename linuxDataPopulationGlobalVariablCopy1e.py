import os
uim_username = os.getenv("uim_username")
uim_password = os.getenv("uim_password")
uimserver = os.getenv("uimserver")
vm_username = os.getenv("vm_username")
vm_password = os.getenv("vm_password")
domain = os.getenv("domain")
uimpath = os.getenv("uimpath")
probe_deactivate = r"""{}/bin/pu -u {} -p {} {}/controller probe_deactivate automated_deployment_engine""".format(uimpath, uim_username, uim_password, domain)
probe_activate = r"""{}/bin/pu -u {} -p {} {}/controller probe_activate automated_deployment_engine""".format(uimpath, uim_username, uim_password, domain)
probe_deploy = r"""{}/bin/pu -u {} -p {} {}/automated_deployment_engine deploy_probe probename""".format(uimpath, uim_username, uim_password, domain)
uimversion = os.getenv("uimversion")
port = 22