# Create gitHub Domain(s)

## DNS

1. Create A records that point to the following addresses:
```
cloudhybrid.io. 	59	IN	A	185.199.108.153
cloudhybrid.io. 	59	IN	A	185.199.109.153
cloudhybrid.io. 	59	IN	A	185.199.110.153
cloudhybrid.io. 	59	IN	A	185.199.111.153
```

2. Create CNAME record for www.

3. Confirm A records were successfully setup.
```
dig +noall +answer [domain.tld]
```

4. Create the custom domain on the repository's gitHub page.

5. Create SSL Certificate.
    - Note, SSL certificates can take up to 24 hours to be issues.
    - https://github.com/cloud-hybrid/Cloud/settings
