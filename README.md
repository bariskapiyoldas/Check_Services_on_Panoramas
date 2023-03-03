# Python Script for Palo Alto Service Check

This script checks if a service exists in Palo Alto firewall, and if it doesn't exist, it creates it. The script requires SSH library paramiko and paramiko_expect.

# Usage

The script requires input from the user as follows:

Username: The username for the firewall login.

Password: The password for the firewall login.

Servicename: The name of the service to be checked (should be in the format t_xxx).

Service: The type of service (tcp or udp).

Port: The port number for the service.

The output of the script is written to a file named "ServiceCheckResult.txt" in the same directory where the script is run.
The output contains information on whether the service already exists, whether it was successfully created, or if there was an error during the creation process.


# Requirements

*Python 3.x

*paramiko

*paramiko_expect

*A Palo Alto firewall