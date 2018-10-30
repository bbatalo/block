import python_hosts
import click
import sys

SITES = ['www.facebook.com', 'www.twitter.com']
HOSTSPATH = None

@click.command()
def main():
    if sys.platform in ('win32', 'cygwin'):
        HOSTSPATH = 'C:\\Windows\\System32\\drives\\etc\\hosts'
    else:
        HOSTSPATH = '/etc/hosts'

    print(HOSTSPATH)

    hosts = python_hosts.Hosts(HOSTSPATH)
    for entry in hosts.entries:
        print(entry)

if __name__ == '__main__':
    main()