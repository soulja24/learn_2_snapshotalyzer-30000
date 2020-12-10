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
def instances():
    """Commands for instances"""

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
    instances()
