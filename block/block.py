import python_hosts
import click
import sys

SITES = [
    "www.facebook.com",
    "twitter.com",
    "www.reddit.com",
    "www.instagram.com",
    "www.goodreads.com",
    "9gag.com",
    "yts.ag",
    "www.snapchat.com",
    "vk.com",
    "www.4chan.com",
    "www.buzzfeed.com",
    "www.flickr.com",
    "news.ycombinator.com",
]

HOSTSPATH = None
if sys.platform in ("win32", "cygwin"):
    HOSTSPATH = "C:/Windows/System32/drivers/etc/hosts"
else:
    HOSTSPATH = "/etc/hosts"


@click.group()
def cli():
    pass


@click.command()
def curated():
    hosts = python_hosts.Hosts(HOSTSPATH)
    for site in SITES:
        new_entry = python_hosts.HostsEntry(
            entry_type="ipv4", address="127.0.0.1", names=[site]
        )
        hosts.add([new_entry])

    try:
        hosts.write()
    except python_hosts.exception.UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command()
def unblock():
    hosts = python_hosts.Hosts(HOSTSPATH)
    for site in SITES:
        hosts.remove_all_matching(name=site)

    try:
        hosts.write()
    except python_hosts.exception.UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command()
def ls():
    print("The following is a list of curated sites.\n")
    for site in SITES:
        print(site)


cli.add_command(curated)
cli.add_command(unblock)
cli.add_command(ls)

if __name__ == "__main__":
    cli()
