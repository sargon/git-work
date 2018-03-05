#!/usr/bin/env  python3

import click
import configparser
import git
import pathlib

@click.group()
def cli():
    pass

def configure_config_file():
    return pathlib.Path("~/.gitwork").expanduser()

def configure_load_config():
    gitwork_config = configure_config_file()
    config = configparser.ConfigParser()
    config.read(gitwork_config)
    return config

def configure_write_config(config):
    gitwork_config = configure_config_file()
    with open(gitwork_config,'w') as f_config:
        config.write(f_config)

def configure_default():
    config = configparser.ConfigParser()
    config['GLOBAL'] = { 'workdir': pathlib.Path("~/workspace") }
    return config

@cli.group("configure")
def configure():
    """
    Configure the meta-git origin-repo and the to use workdirectory.
    """
    gitwork_config = configure_config_file()
    if not gitwork_config.exists():
        click.echo("No configuration found.")
        if click.confirm("Shall I initialise %s" % gitwork_config):
            click.echo("Initialising.\n")
            config = configure_default()
            configure_write_config(config)
        else:
            click.echo("Abort.")
            exit()
    pass

@configure.command("list")
def configure_list():
    """
    Output the current configuration.
    """
    config = configure_load_config()
    for section in config.sections():
        click.echo("%s" % section);
        for kv in config[section].items():
            click.echo("%s: %s" % kv)

@configure.command("set")
@click.argument("key",type=click.STRING)
@click.argument("value",type=click.STRING)
def configure_set(key,value):
    """
    Set a configuration key,value pair.
    """
    config = configure_load_config()

    # TODO Check for valid keys, so we don't collect garbage
    config['GLOBAL'][key] = value

    configure_write_config(config)

@cli.command("sync")
@click.argument("name",nargs=-1,type=click.STRING,required=False)
def sync(name = None):
    """
    Update the state of cloned repository.
    """
    pass

@cli.command("revive")
@click.argument("name",type=click.STRING)
def revive(name):
    """
    Restore a repository from the stored state.
    """
    pass

@cli.command("purge")
@click.argument("name",type=click.STRING)
def purge(name):
    """
    Remove a repository from the workdir, sync it before acting.
    """

@cli.command("add")
@click.argument("name",type=click.STRING)
@click.argument("path",type=click.Path(readable=True))
def add(name,path):
    """
    Start tracking a repository
    """
    path = pathlib.Path(path)
    if not path.exists():
        click.echo("Path %s does not exist, abort!" % path)
    elif not path.is_dir():
        click.echo("Path %s is no directory, abort!" % path)
    repo = git.Repo(str(path.absolute()))
    click.echo(path)
    click.echo("Remotes:")
    for remote in repo.remotes:
        click.echo("%s - " % remote,nl=False)
        click.echo(' ;'.join([url for url in remote.urls]))
        for ref in remote.refs:
          click.echo("%s " % ref,nl=False)
          click.echo(ref.commit)

    click.echo("Heads:")
    for ref in repo.heads:
        click.echo("%s " % ref,nl=False)
        click.echo(ref.commit)


@cli.command("init")
@click.argument("name",type=click.STRING)
def init(name):
    """
    Init a new git repository in your workdir.
    Create directory if it does not exist, otherwise fail.
    """
    pass

@cli.command("list")
def list():
    """
    List all known repositories. Show detailed origin paths when verbose is True.
    """
    pass


if __name__ == "__main__":
    cli()
