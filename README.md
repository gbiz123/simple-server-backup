# simple-server-backup

Backs up remote servers by reading host and device information from a dedicated block in `/etc/hosts`, then cloning each server's disk over SSH using `dd`.

## Requirements

- Linux with SSH client installed
- Root SSH access to each target server
- Sufficient local disk space for full disk images

## Configuration

### 1. Set the backup path

Edit the `BACKUP_PATH` variable at the top of the script to point to your desired local backup directory:

```python
BACKUP_PATH = "/home/youruser/Backup"
```

### 2. Add a backup block to `/etc/hosts`

The script looks for a block delimited by `# BACKUP START` and `# BACKUP END`. Each line in the block follows this format:

```
<ip> <hostname> # <device>
```

Example:

```
# BACKUP START
138.197.107.25 dispersions-db # /dev/vda
93.127.215.242 mailserver # /dev/sda
192.168.1.8 fedora-desktop # /dev/sdb
# BACKUP END
```

## Usage

```bash
python3 backup.py
```

For each host, the script runs the following command:

```bash
ssh root@ "dd if= bs=4M status=progress" | dd of=/path/to/backup/.img bs=4
```

Backup images are saved as `<hostname>.img` in `BACKUP_PATH`.

## Notes

- Root login must be enabled on each remote server (`PermitRootLogin yes` in `sshd_config`)
- Backups are raw disk images — restoring requires `dd` as well
- No compression is applied; image sizes will match the full size of the source device
