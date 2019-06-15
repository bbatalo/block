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

pass_hosts = click.make_pass_decorator(Hosts)


def find_hosts_path():
    HOSTS_PATH = None
    if sys.platform in ("win32", "cygwin"):
        HOSTS_PATH = "C:/Windows/System32/drivers/etc/hosts"
    else:
        HOSTS_PATH = "/etc/hosts"

    return HOSTS_PATH


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = Hosts(find_hosts_path())


@cli.command(help="Block all sites from the curated list of sites.")
@pass_hosts
def block_all(hosts):
    entries = []
    for site in SITES:
        new_entry = HostsEntry(entry_type="ipv4", address="127.0.0.1", names=[site])
        entries.append(new_entry)

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


@cli.command(
    name="block-profile", help="Blocks several websites under a single profile."
)
@click.argument("profile")
@pass_hosts
def block_profile(hosts, profile):
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


@cli.command(name="block-single", help="Block a single site.")
@click.argument("site")
@pass_hosts
def block_single(hosts, site):
    new_entry = HostsEntry(entry_type="ipv4", address="127.0.0.1", names=[site])

    hosts.add([new_entry])

    try:
        hosts.write()
    except UnableToWriteHosts:
        print(
            f"Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@cli.command(help="Unblock all blocked websites.")
@pass_hosts
def unblock_all(hosts):
    for site in SITES:
        hosts.remove_all_matching(name=site)
    try:
        hosts.write()
    except UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@cli.command(help="Specify the profile to unblock.")
@click.argument("profile")
@pass_hosts
def unblock_profile(hosts, profile):
    profile = str.upper(profile)
    for site in PROFILE_SITES[profile]:
        hosts.remove_all_matching(name=site)

    try:
        hosts.write()
    except UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@cli.command(help="Unblock a single website.")
@click.argument("site")
@pass_hosts
def unblock_single(hosts, site):
    hosts.remove_all_matching(name=site)
    try:
        hosts.write()
    except UnableToWriteHosts:
        print(
            "Unable to write to hosts file. Make sure Block has administrator privileges."
        )


@cli.command(help="Prints a curated list of websites that will be blocked by default.")
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


@cli.command(help="Shows the location of used hosts file.")
@pass_hosts
def show_hosts(hosts):
    print(f"Using hosts file located in: {hosts.hosts_path}")


if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter

