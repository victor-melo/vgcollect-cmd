# WARNING, this is a work in progress

# Introduction
vgcollect-cmd is a command like tool for interacting with your vgcollect.com collection

Currently, only searching your collection is currently supported

# Install
Before you begin, you need to create a vgcollect.cfg file with the following contents 

```
[AUTH]
Username=<enter your vgcollect username>
Password=<enter your vgcollect password>
```

Example Command
```
python3 main.py search "final fantasy"
```