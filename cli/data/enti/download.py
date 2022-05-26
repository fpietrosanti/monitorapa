#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import sys
import requests
import datetime
import os
import shutil

def computeOutDir(argv):

    if not os.getcwd() == "/":
        print("\x1b[1m[ \x1b[31mError\x1b[39m ] Please run \x1b[36mcli/\x1b[39m scripts from the root directory\x1b[0m")
        sys.exit(1)

    if not os.path.isdir("out"):
        os.mkdir("out")

    dirName = f"out/{datetime.datetime.utcnow().strftime('%Y-%m-%d')}"

    if not os.path.isdir(dirName):
        os.mkdir(dirName)
        print(f"\x1b[1m[ ℹ️  ] Created \x1b[36m{dirName}\x1b[39m directory\x1b[0m")

    if not os.path.isfile(os.path.join(dirName, "LICENSE.txt")):
        shutil.copy(
            os.path.abspath("LICENSE.txt"),
            os.path.abspath(dirName)
        )

    if not os.path.isfile(os.path.join(dirName, "README.md")):
        with open(os.path.join(dirName, "README.md"), 'w') as readmeFile:
            readmeFile.write(
                f"""
                This folder has been created by MonitoraPA on {os.path.basename(dirName)}.

                The file enti.tsv has been created by AgID and distributed under CC BY 4.0.
                An updated version can be downloaded from https://indicepa.gov.it/ipa-dati/dataset/enti

                Everything else inside this folder can be used under the Hacking License.
                See LICENCE.txt for the exact terms and conditions.

                """
            )

    return dirName

    # if not "check/" in argv[1]:
    #     sys.exit("Missing GDPR compliance check.")

    # if not "out/" in argv[2] or not "enti.tsv" in argv[2]:
    #     sys.exit("Missing enti.tsv path.")

    # check = os.path.splitext(os.path.basename(argv[1]))[0]
    # outDir = os.path.dirname(argv[2])
    # point = os.path.splitext(os.path.basename(argv[0]))[0]

    # dirName = "%s/%s/%s" % (outDir, check, point)

    # if not os.path.isdir(dirName):
    #     os.makedirs(dirName, 0o755)
    # return dirName

def main():
    outDir = computeOutDir(sys.argv)
    
    url = 'https://indicepa.gov.it/ipa-dati/datastore/dump/d09adf99-dc10-4349-8c53-27b1e5aa97b6?bom=True&format=tsv'
    response = requests.get(url, allow_redirects=True)
    result = response.content.replace(b'HTTPS:SISTEMAAMBIENTELUCCA.IT', b'HTTPS://SISTEMAAMBIENTELUCCA.IT')

    with open(f"{outDir}/enti.tsv", "w") as outFile:
        outFile.write(str(result))

    print(f"\x1b[1m[ ✅ ] Done. You can find the dataset at \x1b[36m{outDir}/enti.tsv\x1b[39m directory\x1b[0m")

if __name__ == "__main__":
    try:
        print("\x1b[1m[ ℹ️  ] Started \x1b[36mdownload.py\x1b[39m script\x1b[0m")
        main()
    except KeyboardInterrupt:
        print("\n\x1b[1m[ ❌ ] keyboard interrupt, aborting\x1b[0m")
        sys.exit(1)
