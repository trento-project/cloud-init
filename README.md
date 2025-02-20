# Cloud Init Trento

## Setting up Cloud Init

```
$ sh ./launch-vm -fresh -gui
$ scp -P 2022 cloud-init/cc_trento_web.py geeko@localhost:/home/geeko
# Log in to the VM via the user geeko and password geeko
$ ssh -p 2022 geeko@localhost
# You might need to run
#   ssh-keygen -R '[localhost]:2022'
# Logged in as geeko@localhost at /home/geeko
$ sudo cp cc_trento_web.py /usr/lib/python3.11/site-packages/cloudinit/config/
$ sudo cloud-init single --report -n cc_trento_web
```
## Resetting Cloud Init

```
# Logged in as geeko@localhost at /home/geeko
$ sudo cloud-init clean --logs
# Reboot or run
$ sudo cloud-init init --local
$ sudo cloud-init init
$ sudo cloud-init modules -m init
$ sudo cloud-init modules -m config
$ sudo cloud-init modules -m final
$ sudo cloud-init single --report -n cc_trento_web
```

## Inspect Cloud Init

```
$ sudo cat /var/log/cloud-init.log
$ sudo cat /var/log/cloud-init-output.log
```
