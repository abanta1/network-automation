# Network Automation Scripts

This project contains Python scripts to automate network device configuration backups and deployment.

## Prerequisites

*   Python 3
*   `netmiko`
*   `cryptography`

### Installation

```bash
pip install netmiko cryptography
```

## Setup

The scripts use encrypted credentials stored locally.
*   **Windows:** `%USERPROFILE%\.netmgr\`

On the first run, you will be prompted to enter a username and password, which will be encrypted and saved for future use.

## Usage

### Backup Configurations (`backup_configs.py`)

Backs up the running configuration of specified devices.

**Arguments:**
*   `--ip <IP>`: Single device IP.
*   `--ipfile <FILE>`: File containing list of device IPs.
*   `--type <TYPE>`: Device type (e.g., `cisco_ios`, `juniper_junos`, `cisco_xr`). **Required**.
*   `--outdir <DIR>`: Directory to save backups.
*   `--log`: Enable verbose logging.

**Example:**
```bash
python backup_configs.py --ip 10.0.0.1 --type cisco_ios --outdir ./backups
```

### Push Configurations (`push_config.py`)

Pushes configuration changes or commands to devices.

**Arguments:**
*   `--ip <IP>`: Single device IP.
*   `--file <FILE>`: File containing list of device IPs.
*   `--configfile <FILE>`: File containing commands to run. **Required**.
*   `--type <TYPE>`: Device type (e.g., `cisco_ios`, `juniper_junos`, `cisco_xr`). **Required**.
*   `--config`: Run in configuration mode (`conf t`). If omitted, runs in exec mode or attempts to detect.
*   `--log`: Enable verbose logging.

**Example:**
```bash
python push_config.py --ip 10.0.0.1 --type cisco_ios --configfile commands.txt --config
```