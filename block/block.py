import python_hosts
import click
import sys

SITES = ['www.facebook.com', 'twitter.com']
HOSTSPATH = None

@click.command()
def main():
    if sys.platform in ('win32', 'cygwin'):
        HOSTSPATH = 'C:/Windows/System32/drivers/etc/hosts'
    else:
        HOSTSPATH = '/etc/hosts'

    print(HOSTSPATH)

    hosts = python_hosts.Hosts(HOSTSPATH)
    for site in SITES:
        new_entry = python_hosts.HostsEntry(entry_type='ipv4', address='127.0.0.1', names=[site])
        hosts.add([new_entry])

    hosts.write()

if __name__ == '__main__':
    main()