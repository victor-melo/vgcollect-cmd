# Introduction
vgcollect-cmd is a command like tool for interacting with your vgcollect.com collection

Currently, only searching and backing up your collection is currently supported

# Install
Before you begin, you need to create a vgcollect.cfg file with the following contents in /.config/vgcollect/

```text
[AUTH]
Username=<enter your vgcollect username>
Password=<enter your vgcollect password>
```

Next, create the following directory /var/db/vgcollect and make sure you can read/write to it.

```bash
mkdir /var/db/vgcollect/
```

You will also need to install the following python libraries using either pip or your package manager

```
requests
colorama
```

Example Commands

## Searching 
Searching all games in your collection with "final fantasy" in its title
```bash
./vgc.py search "final fantasy"
```

## Refresh 
Using the refresh flag will force the application to refresh its local cache from vgcollect and search. You can use this to force a refresh of your local database if you just added a new game to your vgcollect database
```bash
./vgc.py refresh search "mario"
```

## Cases
Using the cases flag, you will search for games with missing cases, note that your query searches for platforms, not for the title
```bash
./vgc.py cases search "PS3"
```

## Backup
Backup your collection to a stdout
```bash
./vgc.py backup > vgcollect_backup.csv
```
