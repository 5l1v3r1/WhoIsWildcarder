'''
MIT License

Copyright (c) 2020 @LITTL3FIELD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
'''

import argparse
import subprocess
import logging
import sys

# Colours for console output

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# Function to perform single whois lookup

def whois_single(domain):
  output = subprocess.check_output(["whois", "-h", "whois.internic.net", "-H", "domain " + domain + "*"])
  result = []
  for line in output.splitlines():
    if b"Domain Name" in line:
      result.append(line.split(b": ", 1)[1])
  return result

# Function for multiple inputs

def whois_multiple(domains):
  result = []
  for domain in domains:
    result += whois_single(domain)
  return result

# Read external file with list

def read_filename(filename):
  result = []
  with open(filename) as f:
    for line in f:
      line = line.strip()
      if line.startswith("#") or line == "":
        continue
      result.append(line)
  return result

# Remove whitelisted domains

def removewhitelist(whitelist):
    with open(whitelist, 'r') as f:
        content = f.readlines()
    return content

def main():
    # Argument Parser
    if len(sys.argv) == 1:
        print(bcolors.HEADER + """
 _____                        _   __          ___ _     _                   _           
 |  __ \                      (_)  \ \        / (_) |   | |                 | |          
 | |  | | ___  _ __ ___   __ _ _ _ _\ \  /\  / / _| | __| | ___ __ _ _ __ __| | ___ _ __ 
 | |  | |/ _ \| '_ ` _ \ / _` | | '_ \ \/  \/ / | | |/ _` |/ __/ _` | '__/ _` |/ _ \ '__|
 | |__| | (_) | | | | | | (_| | | | | \  /\  /  | | | (_| | (_| (_| | | | (_| |  __/ |   
 |_____/ \___/|_| |_| |_|\__,_|_|_| |_|\/  \/   |_|_|\__,_|\___\__,_|_|  \__,_|\___|_|   
Run Domain Wildcard Check for .com/.net
@littl3field

optional arguments in order:
  -h, --help    show this help message and exit
  -s SINGLE     Single domain to check, example = -s google (default: None)
  -f FILENAME   File to be checked with one domain per line (default: None)
  -w WHITELIST  Set a file containing whitelisted domains (default: None)
  -o OUTPUT     Set a file to output too (default: None)

        """ + bcolors.ENDC)

    parser = argparse.ArgumentParser(description="Run Domain Wildcard Check for .com/.net", usage="python whoiswildcarder.py", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-s", dest="single", help="Single domain to check, example = -s google !IMPORTANT! do not include TLD")
    parser.add_argument("-f", dest="filename",
                        help="File to be checked with one domain per line. !IMPORTANT! do not include TLD in your list")
    parser.add_argument("-w", dest="whitelist", help="Set a file containing whitelisted domains")
    parser.add_argument("-o", dest="output", help="Set a file to output too")
    args = parser.parse_args()

    # Configure logging

    logging.basicConfig(filename='whoiswildcard.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    logger = logging.getLogger(__name__)

    try:
        1 / 0
    except ZeroDivisionError as err:
        logger.error(err)

    # Perform whois lookups and output results

    if args.single is not None:
        results = whois_single(args.single)
        print(bcolors.OKBLUE + "Wild Carded Domains:" + "\n" + "\n" + str(results) + "\n" + bcolors.ENDC)

        if args.whitelist is not None: #TODO: else statement here as it does not work without a whitelistfile specified
            white = removewhitelist(args.whitelist)
            a = list(set(results) - set(white))
            file = "WhoIsOutput.txt"
            default = open(file, 'a')
            print(bcolors.OKBLUE + "Wild Carded Domains + Whitelist Removed:" + "\n" + "\n" + str(a) + "\n" + bcolors.ENDC)

            if args.output is not None:
                with open(args.output, 'a') as f:
                    for item in a:
                        f.write("%s\n" % str(item))
                    print(bcolors.WARNING + "[i] Saving results to " + str(args.output) + bcolors.ENDC)
            else:
                with default as f:
                    for item in a:
                        f.write("%s\n" % str(item))
                    print(bcolors.WARNING + "[i] Saving results to " + str(file) + bcolors.ENDC)

        if args.output is not None:
            with open(args.output, 'a') as f:
                for item in results:
                    f.write("%s\n" % str(item))
                print(bcolors.WARNING + "[i] Saving results to " + str(args.output) + bcolors.ENDC)
        else:
            file = "WhoIsOutput.txt"
            default = open(file, 'a')
            with default as f:
                for item in results:
                    f.write("%s\n" % str(item))
                print(bcolors.WARNING + "[i] Saving results to " + str(file) + bcolors.ENDC)


    elif args.filename is not None:
        domains = whois_multiple(read_filename(args.filename))
        print(bcolors.OKBLUE + "Wild Carded Domains:" + "\n" + "\n" + str(domains) + "\n" + bcolors.ENDC)

        if args.whitelist is not None: #TODO: else statement here as it does not work without a whitelistfile specified
            white = removewhitelist(args.whitelist)
            a = list(set(domains) - set(white))
            file = "WhoIsOutput.txt"
            default = open(file, 'a')
            print(bcolors.OKBLUE + "Wild Carded Domains + Whitelist Removed:" + "\n" + "\n" + str(a) + "\n" + bcolors.ENDC)

            if args.output is not None:
                with open(args.output, 'a') as f:
                    for item in a:
                        f.write("%s\n" % str(item))
                    print(bcolors.WARNING + "[i] Saving results to " + str(args.output) + bcolors.ENDC)
            else:
                with default as f:
                    for item in a:
                        f.write("%s\n" % str(item))
                    print(bcolors.WARNING + "[i] Saving results to " + str(file) + bcolors.ENDC)

        if args.output is not None:
            with open(args.output, 'a') as f:
                for item in domains:
                    f.write("%s\n" % str(item))
                print(bcolors.WARNING + "[i] Saving results to " + str(args.output) + bcolors.ENDC)
        else:
            file = "WhoIsOutput.txt"
            default = open(file, 'a')
            with default as f:
                for item in domains:
                    f.write("%s\n" % str(item))
                print(bcolors.WARNING + "[i] Saving results to " + str(file) + bcolors.ENDC)

if __name__ == "__main__":
    main()
