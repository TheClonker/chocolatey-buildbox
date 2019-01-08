#!/usr/bin/env python3

import urllib.request, json, hashlib, os, sys

def get_github(repo):
    request = urllib.request.urlopen('https://api.github.com/repos/' + repo + '/releases')
    latest_release = json.loads(request.read().decode())[0]
    version = latest_release['name']
    for asset in latest_release['assets']:
        if asset['browser_download_url'].endswith('.exe'):
            url = asset['browser_download_url']
    return version.replace('v',''), url

def check_chocolatey(id, version):
    try:
        url = '''https://chocolatey.org/api/v2/Packages(Id='{}',Version='{}')'''.format(id, version)
        request = urllib.request.urlopen(url)
        return True
    except urllib.error.HTTPError  as e:
        return False

def get_checksum_of_url(url):
    return "C7927D9939CFE18C1CEE9CE48B884545AC3338A79CC718C3F8EF24FBB32CC3C3"
    file = url.split("/")[-1]
    urllib.request.urlretrieve(url, file)
    checksum = sha256_checksum(file)
    os.remove(file)
    return checksum

def sha256_checksum(file, block_size=65536):
    sha256 = hashlib.sha256()
    with open(file, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
        return sha256.hexdigest().upper()

def build_package(package, version, url, checksum):
    files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]
    print(files)
    print('Build')
    
def main():
    try:
        repo = os.environ['BUILDBOX_REPO']
        package = os.environ['BUILDBOX_PACKAGE']
    except KeyError:
        print('Enviroment Variables missing !')
        sys.exit(1)
    print('Getting latest {} Release...'.format(package))
    version, url = get_github(repo)
    print('Latest Version: {}'.format(version))
    print('Checking if Version exists on Chocolatey')
    exists = check_chocolatey(package, '2.9') #version
    if exists:
        print('Version exists! Nothing to do!')
    else:
        print('Version is not present on Chocolatey! Need to build!')
        checksum = get_checksum_of_url(url)
        build_package(package, version, url, checksum)

if __name__ == '__main__':
    main()