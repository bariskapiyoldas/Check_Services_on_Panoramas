import sys
import paramiko  ###SSH LIBRARY###
from paramiko_expect import \
    SSHClientInteraction  ###TAKES AN ACTION ACCORDING TO INPUT CODE AND PROVIDES STOP THE CODE (expect)###
from re import search
import time
from getpass import getpass

def checkservice(Username, Password, Servicename, Service, Port):
    # Defined Values
    palo_prompt = ".*> "
    configure_prompt = ".*# "
    service_prompt = ".* {"

    # SSH
    SSH = paramiko.SSHClient()
    SSH.load_system_host_keys()
    SSH.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    # Output File
    file = open("ServiceCheckResult.txt", "a")

    # Panorama's

    Panoramas = {"ip addr.": "hostname"}

    try:
        for host in Panoramas:
            print(host)

            SSH.connect(hostname=host, username=Username, password=Password, port=22)
            with SSHClientInteraction(SSH) as command:
                command.expect(palo_prompt, timeout=5)

                if palo_prompt == command.last_match:
                    print(host, "###########Connection to Palo was established.###########")

                    command.send("configure")
                    command.expect(configure_prompt)
                    command.send("show shared service {}".format(Servicename))
                    command.expect(configure_prompt)
                    services = command.current_output_clean

                    services = services.splitlines()

                    service = services[1]

                    if search(service_prompt, service):

                        print(service)
                        print("Service already exists.")
                        file.write(str(Panoramas[host]) + " " + Servicename + " Service already exists\n")

                    else:

                        print("Service should be defined!!!")
                        file.write(str(Panoramas[host]) + " " + Servicename + " Service doesn't exists\n")

                        print("Service definition in progress....")

                        command.send("set shared service {} protocol {} port {}".format(Servicename, Service, Port))
                        command.expect(configure_prompt)
                        command.send("commit")
                        time.sleep(30)  # needs to be checked exact time during implementation and should be optimized
                        command.expect(configure_prompt)
                        command.send("show shared service {}".format(Servicename))
                        command.expect(configure_prompt)

                        newservices = command.current_output_clean
                        newservices = newservices.splitlines()
                        newservice = newservices[1]

                        if search(service_prompt, newservice):

                            print(newservice)
                            print("Service added successfully.")
                            file.write(str(Panoramas[host]) + " " + Servicename + " Service added successfully\n")

                        else:
                            print(service)
                            print("Could not add service, manual check required.")
                            file.write(str(Panoramas[
                                               host]) + " " + Servicename + " Could not add service, manual check required\n")

                            command.send("exit")
                            command.expect(palo_prompt)
                            command.send("exit")


                else:
                    print("##########Connection to Palo was NOT established, "
                          "Please check your User and Pass info!!!###########")
                    file.write(str(Panoramas[host]) + " " + Servicename + " Please check your User and Pass info!!!\n")

    except Exception as Error:
        print(Error)
        file.write(str(Panoramas[
                           host]) + " " + Servicename + " " + "Error Occured. Please check your network connection or User and Pass info!!!\n")
    return 0


if __name__ == '__main__':
    Username = input("Please Enter Your Username :")
    # Password = getpass.getpass(prompt="Please Enter Your Password :")# Hidden Password
    Password = input("Please Enter Your Password :")
    Servicename = input("Please Enter Service Name as t_xxx :")
    Service = input("Please Enter Service as tcp or udp :")
    Port = input("Please Enter Port Number :")

    checkservice(Username, Password, Servicename, Service, Port)

sys.exit()

##barka##
