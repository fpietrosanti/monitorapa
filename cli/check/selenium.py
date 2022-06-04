#!/usr/bin/env python3

# This file is part of MonitoraPA
#
# Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
# Copyright (C) 2022 Leonardo Canello <leonardocanello@protonmail.com>
#
# MonitoraPA is a hack. You can use it according to the terms and
# conditions of the Hacking License (see LICENSE.txt)

import commons
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import sys
import os.path

import socket





def usage():
    print("""
./cli/selenium.py out/$SOURCE/$DATE/dataset.tsv

Where:
- $SOURCE is a folder dedicated to a particular data source
- $DATE is the data source creation date in ISO 8601 format (eg 2022-02-28)
""")
    sys.exit(-1)




def clickConsentButton(url, lineNum, driver):
	# thanks Mauro Gorrino
    consentPath = "//button[contains(translate(., 'ACET', 'acet'), 'accett')]"
    buttons = driver.find_elements_by_xpath(consentPath)
    for button in buttons:
        try:
            driver.execute_script("arguments[0].click()", button)
            print("%s (%s): click on consent" % (url, lineNum))
        except Exception:
            pass
    return len(buttons) > 0


def saveError(lineNum, error):
    fname = '%s/%s.ERR.txt' % (outDir, lineNum)
    with open(fname, 'w') as f:
        f.write(error)


def runCheck(pa, lineNum, script):
    url = pa[29].lower()
    if len(url) == 0:
        return  # nothing to do... not even logging an error...
    if not looksValidUrl(url):
        saveError(lineNum, "invalid url: %s" % url)
        return

    url = normalizeUrl(url)
# Disabled: seemed a good idea, but can take several seconds to timeout
#           anyway and is less stable then the browser anyway
#           (for example the server might resolve to an unreachable
#            ip or redirect to an unreachable host)
#    if not looksReachableUrl(url):
#        saveError(lineNum, "unreachable: %s" % url)
#        return

    op = webdriver.ChromeOptions()
    op.add_argument('--headless')
    op.add_argument('--disable-web-security')
    op.add_argument('--no-sandbox')
    op.add_argument('--disable-extensions')
    op.add_argument('--dns-prefetch-disable')
    op.add_argument('--disable-gpu')
    op.add_argument('--ignore-certificate-errors')
    op.add_argument('--ignore-ssl-errors')
    op.add_argument('enable-features=NetworkServiceInProcess')
    op.add_argument('disable-features=NetworkService')
    op.add_argument('--window-size=1920,1080')
    op.add_argument('--aggressive-cache-discard')
    op.add_argument('--disable-cache')
    op.add_argument('--disable-application-cache')
    op.add_argument('--disable-offline-load-stale-cache')
    op.add_argument('--disk-cache-size=0')

    driver = webdriver.Chrome('chromedriver', options=op)

    try:
        driver.get(url)
        time.sleep(6)
        consented = clickConsentButton(url, lineNum, driver)
        if consented:
            time.sleep(4)
        driver.execute_script(script)
        time.sleep(4)
        fname = '%s/%s.OK.txt' % (outDir, lineNum)
        with open(fname, 'w') as f:
            f.write(driver.title)
        print("%s: found '%s', saved in %s" % (url, driver.title, fname))
        if consented == True:
            fname = '%s/%s.CONSENT.txt' % (outDir, lineNum)
            with open(fname, 'w') as f:
                f.write("")
    except WebDriverException as err:
        saveError(lineNum, "%s\n%s" % (url, err))
    #time.sleep(100000)
    driver.quit()

def loadChecks():
    checksToRun = {}
    files = os.listdir('./cli/check/selenium/')
    for jsFile in files:
        if os.path.isfile(jsFile) and jsFile.endswith('.js')
            js = jsFile.read()
            checksToRun[jsFile] = js
    return checksToRun;

def main(argv):
    
        
    if len(sys.argv) != 2:
        usage()

    dataset = sys.argv[1]

    if not os.path.isfile(dataset):
        print(f"input dataset not found {dataset}");
        usage()
        
    outDir = f"{os.path.dirname(dataset)}/selenium"

    jsChecks = loadChecks()
    

    count = 0
    with open(source, 'r') as f, open(test) as s:
        script = s.read()
        for line in f:
            if count > 0 and count >= starting_index:
                fields = line.split('\t')

                try:
                    runCheck(fields, count, script)
                except (KeyboardInterrupt):
                    print("Esco")
                    break

            count += 1
            if end_index > 0 and count > end_index:
                break



if __name__ == "__main__":
    main(sys.argv)
