# Quick & Dirty PA Web Sin Shamer

Setup python3, selenium and a selenium driver (change python2.py
if you do not want to use cromium driver)

## Fast track

If you are on a Debian stable you can simply

```
apt-get install python3 python3-selenium chromium-driver
```

## Manual installation for Virtual Env of requirements

- [Python3](https://www.python.org)

On Debian install VirtualEnv

```apt-get install python3-venv ```

On Arch Linux
```
pacman -S python3 TODO: Fix to install virtualenv
```

If your Python3 package doesn't bundle Pip, you will have to [install it](https://pip.pypa.io/en/stable/installation/).

### Setup the repo and packages

Clone the repo:
```bash
git clone https://github.com/hermescenter/monitorapa.git
```
Enter the repo directory:
```bash
cd monitorapa
```
Create a Python Virtual Environment:
```bash
python -m venv .venv
```
Activate your environment:

- Windows
  ```bash
  .\.venv\Scripts\activate.bat
  ```
- Linux
  ```bash
  . .venv/bin/activate
  ```

Install the required packages:
```bash
pip install -r /cli/requirements.txt
```


# Script execution

The scripts assume to be run from the repository root.

Since the list of PA is updated daily, all script must be run on the
same copy of the list, to preserve results' meaning.

So the output directory will be created after each the download of the
list with a date in ISO 8601 format (YYYY-MM-DD), and each script will
output in the LAST of such folders in out/ (alphabetically sorted).

So if you want to run a script in a previous date, just rename the
folder with a grain of salt.

## Point 1

```
python3 cli/point1.py
```
Downloads `out/YYYY-MM-DD/enti.tsv`

## Point 2

If you're accessing your machine with SSH is recommended to use tmux so you don´t have to keep the connection alive.

so, first start a tmux session with:
```
tmux new -s monitoraPA
```
if you don't have tmux installed just install it with your package manager!

then:
```
python3 cli/point2.py check/google_analytics.js out/yyyy-mm-dd/enti.tsv [starting_index]
```

If you want to redirect output:
```
python3 -u cli/point2.py check/google_analytics.js out/yyyy-mm-dd/enti.tsv [starting_index [count]] >> out/yyyy-mm-dd/point2.out
```

If you started a tmux session to safely return to terminal press:

`CTRL + B` and then `D` to detach the session

**ONLY after being detached from the session is safe to close SSH connection!**

To attach again to the session type:
```
tmux attach-session -t monitoraPA
```

Check for Google Analytics presence over all the website listed in
`out/YYYY-MM-DD/enti.tsv` (Tab Separated Value).
Other scripts in `check/` can be used instead of `google_analytics.js`.

The software works this way:

1. point2.py open the target websites in the Selenium Driver
   and run the provided JavaScript
2. google_analytics.js contains the JavaScript code used to detect
   Google Analytics. If it find GA, it put the tracking ID (or any
   other metadata) in document's title or empty it if the site is
   free from Google Analytics surveillance.
3. python.py, after 5 seconds, get the title and write it into a file
   in the out/YYYY-MM-DD/point2/google_analytics/ directory named
   after its line number in the `out/YYYY-MM-DD/enti.tsv`
   file, for example out/YYYY-MM-DD/google_analytics/point2/100.OK.txt
   (or out/YYYY-MM-DD/google_analytics/point2/100.ERR.txt in case of error)

Obviously, if GA is not found, the file will be empty.
If GA is found, it will contains the tracking ID (or any other metadata)

The file creation time will be used as the time of the test.

Point 2 can also be run in several parallel chunk by using

```
python3 -u cli/point2parallel.py check/google_analytics.js out/yyyy-mm-dd/enti.tsv chunk_size >> out/yyyy-mm-dd/point2parallel.out
```
In out/yyyy-mm-dd/google_analytics/point2parallel/ several files will 
log the progress of each execution.

## Point 3
```
python3 cli/point3.py check/google_analytics.js out/yyyy-mm-dd/enti.tsv [format]
```

Will produce a new file `out/YYYY-MM-DD/google_analytics/point3/enti.[format]`
enriched as for specification.

Supported format are `tsv` (the default, always produced) or `csv` (TODO) or `json` (TODO).

## Point 4
```
python3 cli/point4.py check/google_analytics.js out/yyyy-mm-dd/enti.tsv time_to_wait_in_seconds
```

Will send an email to the PAs that are still hosting the
Google surveillance tool.
The list of PAs to mail will be read in the output file of `cli/point3.py`

The sender mail and SMTP server must be configured in a configuration
file named `cli/point4.cfg` that must be kept secret.
A sample (mock) configuration is provided in `cli/point4_sample.cfg`


## GA_General.py
```
python3 cli/grafici/GA_General.py
```
This will generate `out/grafici/GA_General.html` wich contains a graph showing how many PA's use GA over time thanks to out multiple scans.

# Docker setup

Getting started with docker is super easy, the only requirements are docker and docker-compose.
To setup the environment just run the script docker.sh like this:
```bash
bash docker.sh
```
The first time you run the script you should answer Y so that the image will be generated otherwise it will fail. When the script is done you will be inside your container with everything you need to try our code.
