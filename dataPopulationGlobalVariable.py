username = "administrator"
password = "interOP@123"
uimserver = '10.17.165.164'
uimpath = r'/W19SERVER1_domain/W19SERVER1_hub/W19SERVER1'
probe_deactivate = r"""C:\PROGRA~1\Nimsoft\bin\pu -u {} -p {} {}/controller probe_deactivate automated_deployment_engine""".format(username, password, uimpath)
probe_activate = r"""C:\PROGRA~1\Nimsoft\bin\pu -u {} -p {} {}/controller probe_activate automated_deployment_engine""".format(username, password, uimpath)
probe_deploy = r"""C:\PROGRA~1\Nimsoft\bin\pu -u {} -p {} {}/automated_deployment_engine deploy_probe probename""".format(username, password, uimpath)
uimversion = 201