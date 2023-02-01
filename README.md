# Change Directory Numbers Route Partition

Python script to change the Route Partition on multiple DNs specified in an input file.

## Contacts

- Gerardo Chaves (gchaves@cisco.com)

## Solution Components

- CUCM
- Python

## Prerequisites

- Python 3 (tested with 3.10)
- A CUCM Environment (VMs included)
- VPN to be on the same network as CUCM
- Optional: Setup a Cisco dCloud demo instance that contains the CUCM VM (the [Cisco Collaboration 14 v1 - Transform Work with Collaboration (TWC)](https://dcloud2-rtp.cisco.com/content/demo/878809) demo is a good environment)

## Getting started

- Install Python 3

  On Windows, choose the option to add to PATH environment variable

- If installing on Linux, you may need to install dependencies for `python3-lxml`, see [Installing lxml](https://lxml.de/3.3/installation.html)

  E.g. for Debian/Ubuntu:

  ```bash
  sudo apt build-dep python3-lxml
  ```

- (Optional) Create/activate a Python virtual environment named `venv`:

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- Install needed dependency packages:

  ```bash
  pip install -r requirements.txt
  ```

- Rename `.env.example` to `.env`, and edit it to specify your CUCM address and AXL user credentials.

- Make sure the user being used has a user rank of 1 or with proper API AXL permissions (Role: Standard AXL API Access Reference: https://www.cisco.com/c/en/us/td/docs/voice_ip_comm/cucm/admin/9_0_1/ccmsys/CUCM_BK_CD2F83FA_00_cucm-system-guide-90/CUCM_BK_CD2F83FA_00_system-guide_chapter_0100.pdf)

- The AXL v14 WSDL files are included in this project. If you'd like to use a different version, replace with the AXL WSDL files for your CUCM version:

  1. From the CUCM Administration UI, download the 'Cisco AXL Tookit' from **Applications** / **Plugins**

  2. Unzip the kit, and navigate to the `schema/current` folder

  3. Copy the three WSDL files to the `schema/` directory of this project: `AXLAPI.wsdl`, `AXLEnums.xsd`, `AXLSoap.xsd`

## Usage

1. Fill out the dn_patterns.txt file with the directory numbers to change the partition on. One per line.

2. Set the PARTITION_NAME constant in the axl_update_Line.py script to the name of the partition you wish to use to set the DNs to.

3. Execute the python script from a terminal:

   $ python axl_update_Line.py

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:

<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
