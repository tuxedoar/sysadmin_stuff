## English description

### ldap-attributes-selector.py

This script allows you to query an LDAP server, based on a custom set of provided attributes. The results are given in CSV format, though they
are not written to a CSV file unless explicitly specified. 

### Requirements
This script should work with, at least, Python 2.7. Make sure you have the [python-ldap](https://pypi.python.org/pypi/python-ldap/) library, installed!.

Also, note that when establishing an SSL connection, depending on the security settings in your LDAP server, you might gonna need to perform some additional
configuration on your LDAP client!.   

As a general rule, if you are able to make an LDAP query with the `ldapsearch` tool, this script should work as well!. 

### How to use it? 
```
Get a CSV formatted list from an LDAP database, given a custom set of provided
attributes.

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        URI formatted address (IP or domain name) of the LDAP
                        server
  -b BASEDN, --basedn BASEDN
                        Specify the searchbase or base DN of the LDAP server
  -u USERDN, --userdn USERDN
                        Distinguished Name (DN) of the user to bind to the
                        LDAP directory
  -a USERATTRS, --userAttrs USERATTRS
                        A set of comma separated LDAP attributes to list
  -S SIZELIMIT, --sizelimit SIZELIMIT
                        Specify the maximum number of LDAP entries to display
                        (Default: 500)
  -f FILTER, --filter FILTER
                        Specify an LDAP filter (Default: 'objectClass=*')
  -w WRITETOCSV, --writetocsv WRITETOCSV
                        Write results to a CSV file!.
```
Note that the following arguments are mandatory: 
 * `--server`/`-s`
 * `--basedn`/`-b`
 * `--userdn`/`-u`
 * `--userAttrs`/`-a`

The rest of them, are optional!.


### Examples
In the following example, an encrypted LDAP query (note the `ldaps://` when specifying the LDAP server) is made, and the attributes `name`, `mail` and `ipPhone` are retrieved. In addition, the search base used is `objectClass=person` and a maximum of 50 entries will be printed!.
```
./ldap-attributes-selector.py -s ldaps://somecorp.com -b "dc=somecorp,dc=com" -u "cn=Joe,ou=Users,dc=somecorp,dc=com" -a "name,mail,ipPhone" -S 50 -f objectClass=person
```

Unlike the previous example, on the next one, the query won't be encrypted; a different LDAP filter is used and no limits on the number of results to display are given, other than the defults (500 entries): 
```
./ldap-attributes-selector.py -s ldap://somecorp.com -b "dc=somecorp,dc=com" -u "uid=zimbra,cn=admins,cn=zimbra" -a "givenName,mail,zimbraAccountStatus" -f 'objectClass=inetOrgPerson'
```

This other example is similar to the first one, except that, this time, the retrieved results, are gonna be exported to a CSV file!: 
```
./ldap-attributes-selector.py -s ldaps://somecorp.com -b "dc=somecorp,dc=com" -u "cn=joe,ou=Users,dc=somecorp,dc=com" -a "name,mail,ipPhone" -S 50 -f objectClass=person -w users.csv
```

In general terms, whenever an entry doesn't have any of the provided LDAP attributes, a "NULL" string, will be printed!.
