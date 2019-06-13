import click
import sys

from python_hosts.hosts import Hosts, HostsEntry
from python_hosts.exception import UnableToWriteHosts

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

PROFILE_SITES = {
    "SOCIAL": [
        "www.facebook.com",
        "twitter.com",
        "www.reddit.com",
        "www.instagram.com",
        "www.goodreads",
        "www.snapchat",
        "vk.com",
        "www.flickr.com",
    ],
    "MEME": ["9gag.com", "www.4chan.com"],
    "NEWS": ["news.ycombinator.com", "blic.rs"],
    "BLOGS": ["www.buzzfeed.com", "ispovesti.com"],
    "ESPORTS": ["www.hltv.org", "www.twitch.tv"],
    "PORN": [],
    "PIRATE": ["yts.ag"],
}

PROFILES = ["SOCIAL", "MEME", "NEWS", "BLOGS", "ESPORTS", "PORN", "PIRATE"]

HOSTS_PATH = None
if sys.platform in ("win32", "cygwin"):
    HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"
else:
    HOSTS_PATH = "/etc/hosts"


@click.group()
def cli():
    pass


@click.command(name="all", help="Block all sites from the curated list of sites.")
def block_all():
    hosts = Hosts(HOSTS_PATH)

    entries = []
    # begin_comment_entry = HostsEntry(
    #     entry_type="comment",
    #     comment="# BLOCK ### This is the beginning of Block entries. ### BLOCK",
    #     names=[],
    # )
    # entries.append(begin_comment_entry)

    for site in SITES:
        new_entry = HostsEntry(entry_type="ipv4", address="127.0.0.1", names=[site])
        entries.append(new_entry)

    # end_comment_entry = HostsEntry(
    #     entry_type="comment",
    #     comment="# BLOCK ### This is the end of Block entries. ### BLOCK",
    #     names=[],
    # )
    # entries.append(end_comment_entry)

    hosts.add(entries)
    try:
        hosts.write()
        print(
            f"All websites in a curated list have been blocked. Please reopen your browser to get rid of cached websites."
        )
        print(f"To see a complete list of blocked websites, type 'block ls'")
    except UnableToWriteHosts:
        print(
            f"Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(
    name="profile",
    help="Blocks a profile of websites, currently this means just the curated list for that profile.",
)
@click.argument("profile")
def block_profile(profile):
    hosts = Hosts(HOSTS_PATH)

    profile = str.upper(profile)

    if profile in PROFILES:
        for site in PROFILE_SITES[profile]:
            new_entry = HostsEntry(entry_type="ipv4", address="127.0.0.1", names=[site])
            hosts.add([new_entry])
    else:
        print(f"No such profile exists, please try again.")

    try:
        hosts.write()
        print(
            f"All websites from the selected profile have been blocked. Please reopen your browser to get rid of cached websites."
        )
        print(
            f"To see a list of websites blocked by current profile, type 'block ls -p 'PROFILE_NAME'"
        )
    except UnableToWriteHosts:
        print(
            f"Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(
    name="single", help="Block a single site, defined by the positional argument."
)
@click.argument("site")
def block_single(site):
    hosts = Hosts(HOSTS_PATH)
    new_entry = HostsEntry(entry_type="ipv4", address="127.0.0.1", names=[site])

    hosts.add([new_entry])

    try:
        hosts.write()
    except UnableToWriteHosts:
        print(
            f"Unable to write to hosts file. Make sure Block has administrator privileges."
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
@click.option(
    "-p",
    "--profile",
    default=None,
    help="Specify the profile to unblock. The command will unblock all websites listed under that profile.",
)
def unblock(site, profile):
    hosts = Hosts(HOSTS_PATH)

    if site is None and profile is None:
        for s in SITES:
            hosts.remove_all_matching(name=s)
    elif site is not None:
        hosts.remove_all_matching(name=site)
    elif profile is not None:
        profile = str.upper(profile)
        for s in PROFILE_SITES[profile]:
            hosts.remove_all_matching(name=s)

    try:
        hosts.write()
    except UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@click.command(
    help="Prints a curated list of websites that will be blocked by default."
)
@click.option(
    "-p",
    "--profile",
    default=None,
    help="List all websites curated under the specified profile.",
)
def ls(profile):

    if profile is not None:
        profile = str.upper(profile)
        for site in PROFILE_SITES[profile]:
            print(site)
    else:
        print(
            "The following is a curated list of websites that will be blocked by default.\n"
        )
        for site in SITES:
            print(site)


cli.add_command(block_all)
cli.add_command(block_profile)
cli.add_command(block_single)
cli.add_command(unblock)
cli.add_command(ls)

if __name__ == "__main__":
    cli()
