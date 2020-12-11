import boto3
#for argv
#import sys
import click

session = boto3.Session(profile_name='shotty')
ec2 = session.resource('ec2')


##little helper filter function to reuse code
## argument project and return instances (list)
def filter_instances(project):
    instances = []
    if project:
        my_filter = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=my_filter)
    else:
        instances = ec2.instances.all()

    return instances

@click.group()
def cli():
    """shotty manages snapshots"""

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, help="Only snapshots for project (tag Project:<name>)")

def list_snapshots(project):
    "List EC2 snapshots"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            for s in v.snapshots.all():
                 print(", ".join((
                    s.id,
                    v.id,
                    i.id,
                    s.state,
                    s.progress,
                    s.start_time.strftime("%c")
                 )))
    return


@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, help="Only volumes for project (tag Project:<name>)")

def list_volumes(project):
    "List EC2 volumes"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            print(", ".join((
                v.id,
                i.id,
                v.state,
                str(v.size) + "GiB",
                v.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('instances')
def instances():
    """Commands for instances"""


@instances.command('snapshot', help="Create snapshots of all volumes")
@click.option('--project', default=None,help="Only create snapshots for project (tag Project:<name>)")

def create_inst_snapshots(project):
    "Create snapshots for EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        for v in i.volumes.all():
            #create snapshot Command
            print("Creating snapshot of {0}".format(v.id))
            v.create_snapshot(Description="Created by SnapshotAlyzer 30000")
    return

#@click.command()
@instances.command('list')
@click.option('--project', default=None,help="Only instances for project (tag Project:<name>)")
#and maybe below can define more instances.command()
#@instances.command('stop') including their own function, below is fucntion for list.
#@instances.command('start')  etc

def list_instances(project):
    "List EC2 instances"

    instances = filter_instances(project)

    for i in instances:
        tags = { t['Key']: t['Value'] for t in i.tags or []}
        #print(i)
        print(', '.join((
        i.id,
        i.instance_type,
        i.placement['AvailabilityZone'],
        i.state['Name'],
        i.public_dns_name,
        tags.get('Project', '<no projecto>')
        )))
    return

@instances.command('stop')
@click.option('--project', default=None,help="Only instances for project")

def stop_instances(project):
    "Stop EC2 instances"

    ##filter code for selecting project (if specified) or all
    #replaced with filter fxn
    instances = filter_instances(project)

    ## once instances obtain, stop code
    for i in instances:
        print("Stopping {0}...".format(i.id))
        i.stop()

    return

@instances.command('start')
@click.option('--project', default=None,help="Only instances for project")

def start_instances(project):
    "Start EC2 instances"

    ##filter code for selecting project (if specified) or all
    ##replaced with filter fxn
    instances = filter_instances(project)

    ## once instances obtain, start code
    for i in instances:
        print("Starting {0}...".format(i.id))
        i.start()

    return

if __name__ == '__main__':
    #print(sys.argv)
    #list_instances()
    #instead of single fxn, setup the group
    cli()
