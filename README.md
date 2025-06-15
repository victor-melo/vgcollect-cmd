# WARNING, this is a work in progress

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

Example Command
```
# Display all games in your collection with "final fantasy" in its title
./vgc.py search "final fantasy"

# Using the use_local flag will cause the application to use its local cache to search instead
# of reaching out to vgcollect.com. Use this to increase search speed if you havent updated your
# vgcollect database since your last search
./vgc.py use_local search "mario"

# Using the cases flag, you will search for games with missing cases, note that your query searches
# for platforms, not for the title
./vgc.py cases search "PS3"

# Backup your collection to a csv file
./vgc.py backup
```
