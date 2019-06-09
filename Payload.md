# Development

## Critical
 - [ ] Implement docstring format top-level objects:
```
Remote-Host Object for KVM-Based Hosting

Host.py serves as the mothership for our cloud-provisioning tool. This 
module is responsible for securing remote connections, creating 
required services (SQL, Reverse-Proxies, Email, Webservers, etc.) & 
hosting our Virtual Private Servers (VPS).

@Structure
  Host(object):
    :Parameters:
      - user          :     (String)     :     Host login name
      - server        :     (String)     :     Local IP address
      - OS            :     (String)     :     TBD

@Dependencies
  - TBD

@Attributes
  - N/A : (None) : N/A

@Functions
    - function(input:type): 
      ...

@General
  - Contact: development.cloudhybrid@gmail.com (Snow)
  - Documentation: https://github.com/cloud-hybrid/Payload
  - Website: https://vaultcipher.com/

@Development
  - [ ] Implement linux & windows port in single python program.
  - [ ] Use OS to check Host and Remote-Host operating system and
          return information for error checking in global namespace.
```

 - [ ] Ensure objection structure functions go instance functions -> staticmethods -> classmethods.

 - [ ] When creating FTP account, disable create FTP User button and add spining wheel upon click. 
 
## Important

## Minor
- [ ] Create UML Object Diagram.
  - [ ] Ensure Ctypes and other optimization programs are implemented in all.

- [ ] Add Discord server to README.md.

## Indeterminate

# Support & Documentation

## Dependencies
Graphviz for Windows: https://graphviz.gitlab.io/_pages/Download/windows/graphviz-2.38.msi
gprof2dot: https://github.com/jrfonseca/gprof2dot



## Quick Reference

### Class Methods
The @classmethod decorator, is a builtin function decorator that is an expression that gets evaluated after your function is defined. The result of that evaluation shadows your function definition.
A class method receives the class as implicit first argument, just like an instance method receives the instance.
```
class C(object):
    @classmethod
    def fun(cls, arg1, arg2, ...):
```
 - A class method is a method which is bound to the class and not the object of the class.
 - They have the access to the state of the class as it takes a class parameter that points to the class and not the object instance.
 - It can modify a class state that would apply across all the instances of the class. For example it can modify a class variable that will be applicable to all the instances.

### Static Methods
A static method does not receive an implicit first argument.
```
class C(object):
    @staticmethod
    def fun(arg1, arg2, ...):
```
 - A static method is also a method which is bound to the class and not the object of the class.
 - A static method can’t access or modify class state.
 - In general, static methods know nothing about class state. They are utility type methods that take some parameters and work upon those parameters. On the other hand class methods must have class as parameter.

### Subprocess
- subprocess.call() will spawn a new process, pause the program, execute the input on said new process, and then resume the program. 

- subprocess.run() will execute a subprocess in parallel. 
## Languages
- [Python3.6+](https://docs.python.org/3/) - Programming Language
- [Bash](https://www.tldp.org/LDP/abs/abs-guide.pdf) - Scripting Language
- [PHP 7.2+](http://php.net/manual/en/install.php) - Front/Backend Development Language

## Infrastructure
* [Nginx](https://docs.python.org/3/) - Reverse Proxy, SSL Encryption, SSH Jump-Server
* [Apache 2.4+](https://httpd.apache.org/docs/2.4/) - Backend Webserver, PHP 7.2 FPM Proxy
  * [CGI](https://httpd.apache.org/docs/2.4/mod/mod_cgi.html) - Apache2 Scripting Module

## Author(s) & Acknowledgments

* **Jacob B. Sanders** - *Project Creator, Owner of Vault Cipher LLC.* - [Vault Cipher LLC.](https://vaultcipher.com/team/jacob-sanders)

* [Contributors & Contributions](https://github.com/vaultcipher/Payload/Contributors)

## License