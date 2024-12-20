import pulumi
import pulumi_aws as aws

config = pulumi.Config()

region = "ap-southeast-1"
env = "todo-infra-dev"
cidr_block = "10.10.0.0/16"  # vpc cidr

public_subnet_1_cidr = (
    "10.10.1.0/24"  # bastion server in this sn, also the client app is deployed.
)
public_subnet_2_cidr = "10.10.2.0/24"

private_subnet_1_cidr = "10.10.3.0/24"
private_subnet_2_cidr = "10.10.4.0/24"
private_subnet_3_cidr = "10.10.5.0/24"

# A General overview
"""
1 vpc

2 public subnets: 
    - 1st subnet: for alb, bastion server to ssh into provate subnet's ec2 instances, and client app 
    - 2nd subnet: for alb 
    
3 private subnets:
    - 1st: for django app 
    - 2nd for django app 
    - 3rd for pg db 
 
1 igw

1 public and 1 private rtb  

4 ec2 instances: 
    - 1 for bastion server and client app (public sn-1), 2 for django app (private-sn-1 and 2), 1 for pg db (private-sn-3)

4 sg 
1 nat 
1 alb 
1 target group
1 listener
1 key pair  
1 asg 

and all other netwokring association

flow: 

ssh from local host into bastion. 
for availability - from bastion only, ssh into 3 private-sn instances in three different subnets 
app servers only receive traffic from alb 
db only entertain app server cidr 
for scalability - asg for auto scaling that is attached to the alb 
and all other netwokring association

please take a look below to learn more

"""

######################################## BEGIN of Script ########################################

# vpc
vpc = aws.ec2.Vpc(
    f"{env}-vpc",
    cidr_block=cidr_block,
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={"Name": f"{env}-vpc"},
)

# subnet - publix sbnets in two AZs
public_subnet_1 = aws.ec2.Subnet(
    f"{env}-public-sn-1",
    vpc_id=vpc.id,
    cidr_block=public_subnet_1_cidr,
    availability_zone=f"{region}a",
    map_public_ip_on_launch=True,
    tags={"Name": f"{env}-public-sn-1"},
)

public_subnet_2 = aws.ec2.Subnet(
    f"{env}-public-sn-2",
    vpc_id=vpc.id,
    cidr_block=public_subnet_2_cidr,
    availability_zone=f"{region}b",
    map_public_ip_on_launch=True,
    tags={"Name": f"{env}-public-sn-2"},
)

# private subnets in three AZs. first two private subnets are for djago apps, and the 3rd on e is for the pg db
private_subnet_1 = aws.ec2.Subnet(
    f"{env}-private-app-sn-1",
    vpc_id=vpc.id,
    cidr_block=private_subnet_1_cidr,
    availability_zone=f"{region}a",
    map_public_ip_on_launch=False,
    tags={"Name": f"{env}-private-app-sn-1"},
)

private_subnet_2 = aws.ec2.Subnet(
    f"{env}-private-app-sn-2",
    vpc_id=vpc.id,
    cidr_block=private_subnet_2_cidr,
    availability_zone=f"{region}b",
    map_public_ip_on_launch=False,
    tags={"Name": f"{env}-private-app-sn-2"},
)

# private subnet for pg db
private_subnet_for_db = aws.ec2.Subnet(
    f"{env}-private-db-sn-1",
    vpc_id=vpc.id,
    cidr_block=private_subnet_3_cidr,
    availability_zone=f"{region}c",
    map_public_ip_on_launch=False,
    tags={"Name": f"{env}-private-db-sn-1"},
)

# igw
igw = aws.ec2.InternetGateway(f"{env}-igw", vpc_id=vpc.id, tags={"Name": f"{env}-igw"})

# public rt and associatation with public sn
public_route_table = aws.ec2.RouteTable(
    f"{env}-public-rt-1",
    vpc_id=vpc.id,
    routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    tags={"Name": f"{env}-public-rt-1"},
)

aws.ec2.RouteTableAssociation(
    f"{env}-public-rt-association-1",
    subnet_id=public_subnet_1.id,
    route_table_id=public_route_table.id,
)

aws.ec2.RouteTableAssociation(
    f"{env}-public-rt-association-2",
    subnet_id=public_subnet_2.id,
    route_table_id=public_route_table.id,
)

# privaet route table
private_route_table = aws.ec2.RouteTable(
    f"{env}-private-rt-1",
    vpc_id=vpc.id,
    tags={"Name": f"{env}-private-rt-1"},
)

# NAT - NAT in punlic subnet 1
eip = aws.ec2.Eip(f"{env}-nat-eip", vpc=True)

nat_gateway = aws.ec2.NatGateway(
    f"{env}-nat-gateway",
    allocation_id=eip.id,
    subnet_id=public_subnet_1.id,
    tags={"Name": f"{env}-nat-gateway"},
)

# prvate rt and nat gw accociation
aws.ec2.Route(
    f"{env}-private-route-to-nat",
    route_table_id=private_route_table.id,
    destination_cidr_block="0.0.0.0/0",
    nat_gateway_id=nat_gateway.id,
)


# dj app private subnet and priteve rt association
aws.ec2.RouteTableAssociation(
    f"{env}-private-rt-association-1",
    subnet_id=private_subnet_1.id,
    route_table_id=private_route_table.id,
)

aws.ec2.RouteTableAssociation(
    f"{env}-private-rt-association-2",
    subnet_id=private_subnet_2.id,
    route_table_id=private_route_table.id,
)

# db subnet and private rt association
aws.ec2.RouteTableAssociation(
    f"{env}-private-rt-association-3",
    subnet_id=private_subnet_for_db.id,
    route_table_id=private_route_table.id,
)

# sg:

# public sg to access bastion server public sg.
# as we want to ssh from local machine to bastion server, allowing dynamic ip as this would be attachdd tot he public subnet 1
# wher the bstion server is located
public_sn_security_group = aws.ec2.SecurityGroup(
    f"{env}-public-sn-sg",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": ["0.0.0.0/0"],
        },  # allow ssh from local host to bastion server
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
    tags={"Name": f"{env}-app-sg"},  # change the app into sn
)

# alb sg
alb_security_group = aws.ec2.SecurityGroup(
    f"{env}-alb-sg",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        },
        {
            "protocol": "tcp",
            "from_port": 443,
            "to_port": 443,
            "cidr_blocks": ["0.0.0.0/0"],
        },
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
    tags={"Name": f"{env}-alb-sg"},
)

# dj app sg
app_security_group = aws.ec2.SecurityGroup(
    f"{env}-app-sg",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "security_groups": [alb_security_group.id],
        },
        {
            "protocol": "tcp",
            "from_port": 443,
            "to_port": 443,
            "security_groups": [alb_security_group.id],
        },
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": [
                public_subnet_1_cidr
            ],  # 10.10.1.0/24 - only from public subnet 1 cidr, i.e. the bastion server can ssh
        },
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
    tags={"Name": f"{env}-app-sg"},
)

# pg db server sg
db_security_group = aws.ec2.SecurityGroup(
    f"{env}-db-sg",
    vpc_id=vpc.id,
    ingress=[
        {
            "protocol": "tcp",
            "from_port": 5432,
            "to_port": 5432,
            "security_groups": [app_security_group.id],
        },
        {
            "protocol": "tcp",
            "from_port": 22,
            "to_port": 22,
            "cidr_blocks": [
                public_subnet_1_cidr
            ],  # 10.10.1.0/24 - only from public subnet 1 cidr, i.e. the bastion server can ssh
        },
    ],
    egress=[
        {"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}
    ],
    tags={"Name": f"{env}-db-sg"},
)

ubuntu_ami_id = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {
            "name": "name",
            "values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"],
        },
    ],
).id

key_pair = aws.ec2.KeyPair(
    f"{env}-keyname",
    key_name="aws-infra-todo-app-keypair",
    public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCQWXN6x3aCo5J7YKtq+yuDqiK5MT4In46TO4fuWWBhZuyB1GUa/uov0Nzu8+IjS/7hMvRZuhbMDe1olJuPHc0vPpuORjsOac/46ayZ02Mu7RIzGVhA0Z+dSobHkO4+hVc2HduhXWnvhYQfClV1ozvNctQhe+xCDiCFScC201vZAHczLY4ak9PNkN/qEf/I47E+VOp+BD53ld90GoiK27wExX0Q5EUXbn7ATznHA7RRP6vsyt7wL7RCOE3quxsjNvaS3et00mG9dpN+CEYemlFXii8lopHMpJV30+96ypbPyVLXGjhVd8V7mTvQJoHgsYS36R/gal+TieeEVD7YG/CD mehboob@pop-os",
)

# bastion server tossh into the private sbn servers
bastion_instance = aws.ec2.Instance(
    f"{env}-bastion-instance",
    instance_type="t2.micro",
    ami=ubuntu_ami_id,
    subnet_id=public_subnet_1.id,
    vpc_security_group_ids=[public_sn_security_group.id],
    key_name=key_pair.key_name,
    tags={"Name": f"{env}-bastion-instance"},
)

# privae sn instances for dj app
django_instance_1 = aws.ec2.Instance(
    f"{env}-django-instance-1",
    instance_type="t2.micro",
    ami=ubuntu_ami_id,
    subnet_id=private_subnet_1.id,
    vpc_security_group_ids=[app_security_group.id],
    key_name=key_pair.key_name,
    tags={"Name": f"{env}-django-instance-1"},
)

django_instance_2 = aws.ec2.Instance(
    f"{env}-django-instance-2",
    instance_type="t2.micro",
    ami=ubuntu_ami_id,
    subnet_id=private_subnet_2.id,
    vpc_security_group_ids=[app_security_group.id],
    key_name=key_pair.key_name,
    tags={"Name": f"{env}-django-instance-2"},
)

pgdb_instance_1 = aws.ec2.Instance(
    f"{env}-pg-db-instance-1",
    instance_type="t2.micro",
    ami=ubuntu_ami_id,
    subnet_id=private_subnet_for_db.id,
    vpc_security_group_ids=[db_security_group.id],
    key_name=key_pair.key_name,
    tags={"Name": f"{env}-pg-db-instance-1"},
)


# alb
# tg for alb
target_group = aws.lb.TargetGroup(
    f"{env}-tg",
    port=80,
    protocol="HTTP",
    vpc_id=vpc.id,
    target_type="instance",
    health_check={
        "path": "/api/v1/common/healthcheck/",
        "interval": 60,
        "timeout": 5,
        "healthy_threshold": 2,
        "unhealthy_threshold": 5,
    },
    tags={"Name": f"{env}-tg"},
)

instance_tg_attachment_1 = aws.lb.TargetGroupAttachment(
    f"{env}-instance-tg-attachment-1",
    target_group_arn=target_group.arn,
    target_id=django_instance_1.id,
    port=80,
)
instance_tg_attachment_2 = aws.lb.TargetGroupAttachment(
    f"{env}-instance-tg-attachment-2",
    target_group_arn=target_group.arn,
    target_id=django_instance_2.id,
    port=80,
)

alb = aws.lb.LoadBalancer(
    f"{env}-alb",
    internal=False,
    security_groups=[alb_security_group.id],
    subnets=[public_subnet_1.id, public_subnet_2.id],
    enable_deletion_protection=False,
    tags={"Name": f"{env}-alb"},
)


listener = aws.lb.Listener(
    f"{env}-alb-listener",
    load_balancer_arn=alb.arn,
    port=80,
    protocol="HTTP",
    default_actions=[
        {
            "type": "forward",
            "target_group_arn": target_group.arn,
        }
    ],
    tags={"Name": f"{env}-listener"},
)

# asg
# user data for asg lt (praepares teh environemnt for new instance, installes the todo app and rungs the docker compose)
user_data = """#!/bin/bash
set -o errexit
set -o nounset

sudo apt update -y
sudo apt upgrade -y
sudo apt install -y python3 python3-pip git nginx curl
sudo apt install -y ca-certificates curl gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update -y
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
sudo usermod -aG docker ubuntu
newgrp docker

export DATABASE_URL="postgres://tododbuser:todopgpass123@10.10.5.10:5432/tododb"
cd /home/ubuntu/
git clone https://github.com/Mahboob-A/sys-design-scalable-aws-env-backend.git
cd src/
docker compose -p todo_app_backend -f dev.yml up --build -d --remove-orphans &
"""

# launch template
launch_template = aws.ec2.LaunchTemplate(
    f"{env}-django-app-lt",
    name=f"{env}-django-app-lt",
    image_id=ubuntu_ami_id,
    instance_type="t2.micro",  
    key_name=key_pair.key_name,
    user_data=user_data, 
    network_interfaces=[
        {
            "associate_public_ip_address": False,
            "security_groups": [app_security_group.id],
            "subnet_id": private_subnet_1.id,
        }
    ],
    tags={"Name": f"{env}-django-app-lt"},
)

# asg
asg = aws.autoscaling.Group(
    f"{env}-django-app-asg",
    vpc_zone_identifiers=[private_subnet_1.id, private_subnet_2.id],
    desired_capacity=2,
    min_size=1,
    max_size=5,
    launch_template={
        "id": launch_template.id,
        "version": "$Latest",
    },
    target_group_arns=[target_group.arn],  
    tags=[
        {
            "key": "Name",
            "value": f"{env}-django-instance-managad-by-asg",
            "propagate_at_launch": True,
        }
    ],
)

# policirs
scale_up_policy = aws.autoscaling.Policy(
    f"{env}-django-asg-scale-up",
    scaling_adjustment=1,
    adjustment_type="ChangeInCapacity",
    cooldown=300,
    autoscaling_group_name=asg.name,
)

scale_down_policy = aws.autoscaling.Policy(
    f"{env}-django-asg-scale-down",
    scaling_adjustment=-1,
    adjustment_type="ChangeInCapacity",
    cooldown=300,
    autoscaling_group_name=asg.name,
)


# infra
pulumi.export("vpc_id", vpc.id)
pulumi.export("public_subnet_1", public_subnet_1.id)
pulumi.export("public_subnet_2", public_subnet_2.id)

# netwokring
pulumi.export("igw_id", igw.id)
pulumi.export("public_route_table", public_route_table.id)

# ec2
pulumi.export("django_instance_1", django_instance_1.id)
pulumi.export("django_instance_2", django_instance_2.id)

# alb
pulumi.export("target_group_id", target_group.id)
pulumi.export("alb.id", alb.id)
pulumi.export("alb_dns_name", alb.dns_name)
pulumi.export("listener_id", listener.id)

# asg
pulumi.export("asg_name", asg.name)
pulumi.export("asg_arn", asg.arn)
pulumi.export("asg_id", asg.id)
pulumi.export("asg_launch_template_id", launch_template.id)


######################################## END of Script ########################################
