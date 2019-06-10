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
    "ispovesti.com",
    "blic.rs",
    "www.hltv.org",
    "www.twitch.tv",
]

HOSTS_PATH = None
if sys.platform in ("win32", "cygwin"):
    HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"
else:
    HOSTS_PATH = "/etc/hosts"


@click.group()
def cli():
    pass


@click.command(help="Block all sites from the curated list of sites.")
def all():
    hosts = python_hosts.Hosts(HOSTS_PATH)

    entries = []
    begin_comment_entry = python_hosts.HostsEntry(
        entry_type="comment",
        comment="# BLOCK ### This is the beginning of Block entries. ### BLOCK",
        names=[],
    )
    # hosts.add([begin_comment_entry])
    entries.append(begin_comment_entry)

    for site in SITES:
        new_entry = python_hosts.HostsEntry(
            entry_type="ipv4", address="127.0.0.1", names=[site]
        )
        # hosts.add([new_entry])
        entries.append(new_entry)

    end_comment_entry = python_hosts.HostsEntry(
        entry_type="comment",
        comment="# BLOCK ### This is the end of Block entries. ### BLOCK",
        names=[],
    )
    # hosts.add([end_comment_entry])
    entries.append(end_comment_entry)

    hosts.add(entries)

    print(hosts.entries)

    try:
        hosts.write()
        print(
            f"All websites in a curated list have been blocked. Please reopen your browser to get rid of cached websites."
        )
        print(f"To see a complete list of blocked websites, type 'block ls'")
    except python_hosts.exception.UnableToWriteHosts:
        print(
            f"Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(help="Block a single site, defined by the positional argument.")
@click.argument("site")
def single(site):
    hosts = python_hosts.Hosts(HOSTS_PATH)
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


@click.command(
    help="Unblock sites from the curated list of sites. Optionally, unblock a single site."
)
@click.option(
    "-s",
    "--site",
    default=None,
    help="Specify the site to unblock. The command will unblock the specified site only.",
)
def unblock(site):
    hosts = python_hosts.Hosts(HOSTS_PATH)

    if site is None:
        for s in SITES:
            hosts.remove_all_matching(name=s)
    else:
        hosts.remove_all_matching(name=site)

    try:
        hosts.write()
    except python_hosts.exception.UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(
    help="Prints a curated list of websites that will be blocked by default."
)
def ls():
    print(
        "The following is a curated list of websites that will be blocked by default.\n"
    )
    for site in SITES:
        print(site)


cli.add_command(all)
cli.add_command(single)
cli.add_command(unblock)
cli.add_command(ls)

if __name__ == "__main__":
    cli()
