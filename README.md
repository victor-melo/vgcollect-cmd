# WARNING, this is a work in progress

# Introduction
vgcollect-cmd is a command like tool for interacting with your vgcollect.com collection

Currently, only searching and backing up your collection is currently supported

# Install
Before you begin, you need to create a vgcollect.cfg file with the following contents 

```
[AUTH]
Username=<enter your vgcollect username>
Password=<enter your vgcollect password>
```

Example Command
```
# Display all games in your collection with "final fantasy" in its title
./vgc.py search "final fantasy"

# Backup your collection to a csv file
./vgc.py backup
```
