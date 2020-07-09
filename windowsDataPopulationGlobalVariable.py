import os
uimUsername = os.getenv("uimUsername")
uimPassword = os.getenv("uimPassword")
uimServer = os.getenv("uimServer")
uimServerLoginName = os.getenv("uimServerLoginName")
uimServerLoginPassword = os.getenv("uimServerLoginPassword")
fileShareIP = "10.17.172.178"
fileShareUserName = "administrator"
fileSharePassword = "interOP@123"
hostName = os.getenv("hostName")
domain = os.getenv("domain")
uimPath = os.getenv("uimPath")
probe_status = r"""{}\bin\pu -u {} -p {} {}/controller probe_status automated_deployment_engine""".format(uimPath, uimUsername, uimPassword, domain)
probe_deactivate = r"""{}\bin\pu -u {} -p {} {}/controller probe_deactivate automated_deployment_engine""".format(uimPath, uimUsername, uimPassword, domain)
probe_activate = r"""{}\bin\pu -u {} -p {} {}/controller probe_activate automated_deployment_engine""".format(uimPath, uimUsername, uimPassword, domain)
probe_deploy = r"""{}\bin\pu -u {} -p {} {}/automated_deployment_engine deploy_probe probename""".format(uimPath, uimUsername, uimPassword, domain)
uimVersion = os.getenv("uimVersion")