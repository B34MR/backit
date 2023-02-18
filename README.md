![Supported Python versions](https://img.shields.io/badge/python-3.9-green.svg)

# backit
A simple backup script used for Pentest projects.
+ Use a custom list of files and directories for backup job.
+ Generates logfile.
+ E-mail logfile option available.
+ Uses TAR Format.
<br>

**Developed and Tested on:**
```
Kali-Linux
```

**Installation:**
```
This project only uses modules from the Python Standard Library.
No installation is required.
```

**Usage:**
```
Usage Examples:
  python backit.py configs/pentest.ini
  python backit.py configs/pentest.ini --sendlog
  python backit.py configs/pentest.ini --keeplog --sendlog --showlog
```

**Configuration File:**
<br>
This project contains a ConfigParser ini file for configuring its options.<br>
The ConfigParser's delimiter is set to '=', which delineates the key and value pair for each option. (I.e The SMTP Settings options would be configured as "host = smtp.gmail.com" and "port = 587").<br>
However, the Source and Destination options do not require a parameter value, therefore the '=' delimter is not used for those options.<br>
<br>
The default configuration file located at '.configs/pentest.ini' is simply a template, modify or create new templates as desired.<br>
```
### Default configuration file ###

# Source files and directories to backup.
[source]
/opt/EyeWitness/Python/
/opt/metasploit4/config/database.yml
/opt/Responder/logs/
/opt/Responder/Responder.db
/opt/scanman/.scanman.db
/root/.cme/logs/
/root/.cme/workspaces/
/usr/share/metasploit-framework/config/database.yml

# Destination backup filepath.
[destination]
/opt/backups

# SMTP Server Settings.
[smtp_settings]
host = 
port =

# SMTP Credentials.
[smtp_auth]
username = 
password = 

# SMTP Headers.
[smtp_headers]
from = 
to = 
subject = 
```