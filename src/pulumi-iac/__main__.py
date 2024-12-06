"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws 


''' 051224, Thursday, 11.00 pm 

The below script creates an aws infra environment with the below specs: 

1 vpc, 2 subnets, 1 igw, 1 rtb, 2 ec2 instances, 1 alb, 1 target group, 1 listener, key pair and all the attachments. 

'''


# A. Infra

# vpc
vpc = aws.ec2.Vpc('poridhi-exam-dev-vpc', 
                cidr_block="10.10.0.0/16", 
                enable_dns_hostnames=True, 
                enable_dns_support=True, 
                tags={"Name": "poridhi-exam-dev-vpc"}
        )

# subnet
subnet1 = aws.ec2.Subnet("poridhi-exam-sb-1a", 
                vpc_id=vpc.id, 
                cidr_block="10.10.1.0/24", 
                availability_zone="ap-south-1a", 
                tags={"Name": "poridhi-exam-sb-1a"}
        )

subnet2 = aws.ec2.Subnet("poridhi-exam-sb-1b", 
                vpc_id=vpc.id, 
                cidr_block="10.10.2.0/24", 
                availability_zone="ap-south-1b", 
                tags={"Name": "poridhi-exam-sb-1b"}
        )

# B. Netowrking
# igw
igw = aws.ec2.InternetGateway("poridhi-exam-igw", 
        vpc_id=vpc.id, 
        tags={"Name": "poridhi-exam-igw"}
)

# route table with igw route
rtb = aws.ec2.RouteTable("poridhi-exam-rtb",  # no need to match this name and tag name
                vpc_id=vpc.id, 
                routes=[{
                        "cidr_block": "0.0.0.0/0", 
                        "gateway_id": igw.id  # gateway attached 
                }],
                tags={"Name": "poridhi-exam-rtb"}  # this tag name is populated as the resource name in aws
        )

# rtb subnet association
rtb_sb_association1= aws.ec2.RouteTableAssociation("poridhi-rta-1a", 
                subnet_id=subnet1.id, 
                route_table_id=rtb.id
        )

rtb_sb_association2 = aws.ec2.RouteTableAssociation("porisdi-rta-1b", 
                subnet_id=subnet2.id, 
                route_table_id=rtb.id        
        )


# C. EC2 Instance

# NOTE: need to recreate the key pair depending on host being used (if poridhi code-server is used, regenerate it, and share the pub key)
key_pair = aws.ec2.KeyPair(
    "poridhi-exam-ec2-keypair",  # can be any name
    key_name="poridhi-exam-ec2-keypair",
    public_key="ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCQWXN6x3aCo5J7YKtq+yuDqiK5MT4In46TO4fuWWBhZuyB1GUa/uov0Nzu8+IjS/7hMvRZuhbMDe1olJuPHc0vPpuORjsOac/46ayZ02Mu7RIzGVhA0Z+dSobHkO4+hVc2HduhXWnvhYQfClV1ozvNctQhe+xCDiCFScC201vZAHczLY4ak9PNkN/qEf/I47E+VOp+BD53ld90GoiK27wExX0Q5EUXbn7ATznHA7RRP6vsyt7wL7RCOE3quxsjNvaS3et00mG9dpN+CEYemlFXii8lopHMpJV30+96ypbPyVLXGjhVd8V7mTvQJoHgsYS36R/gal+TieeEVD7YG/CD mehboob@pop-os",
)

# sg for ec2 and alb
security_group = aws.ec2.SecurityGroup("poridhi-exam-sg", 
                description="poridhi-exam-sg",
                vpc_id=vpc.id, 
                ingress=[
                        {
                                "protocol": "tcp", 
                                "from_port": 22, 
                                "to_port": 22, 
                                "cidr_blocks": ["0.0.0.0/0"], 
                        }, 
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
                                "cidr_blocks": ["0.0.0.0/0"]
                        }
                
                ],  
                egress=[{
                        "protocol": "-1", # all protocols 
                        "from_port": 0, # all port 
                        "to_port": 0, 
                        "cidr_blocks": ["0.0.0.0/0"]
                }], 
                tags={"Name": "poridhi-exam-sg"}
                
        )

# ami_id = "ami-03f4878755434977f"  | same image as below (image of servers) (ubuntu 22.04)
ami_id = aws.ec2.get_ami(most_recent=True, 
                owners=["amazon"], 
                filters=[{
                        "name": "name",
                        "values": ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
                }]
        ).id


ec2_instance1 = aws.ec2.Instance("poridhi-exam-instance-backend-1a", 
        instance_type="t2.micro", 
        ami=ami_id, 
        subnet_id=subnet1.id, 
        vpc_security_group_ids=[security_group.id],
        key_name=key_pair.key_name,
        associate_public_ip_address=True, 
        tags={"Name": "poridhi-exam-instance-backend-1a"}
)


ec2_instance2 = aws.ec2.Instance("poridhi-exam-instance-backend-1b", 
        instance_type="t2.micro", 
        ami=ami_id, 
        subnet_id=subnet2.id, 
        vpc_security_group_ids=[security_group.id],
        key_name=key_pair.key_name,
        associate_public_ip_address=True, 
        tags={"Name": "poridhi-exam-instance-backend-1b"}
)

ec2_instance2 = aws.ec2.Instance("poridhi-exam-instance-client-1a", 
        instance_type="t2.micro", 
        ami=ami_id, 
        subnet_id=subnet2.id, 
        vpc_security_group_ids=[security_group.id],
        key_name=key_pair.key_name,
        associate_public_ip_address=True, 
        tags={"Name": "poridhi-exam-instance-client-1a"}
)


# D. Target gorup and alb 

target_group_tg = aws.lb.TargetGroup("poridhi-exam-tg", 
        vpc_id=vpc.id, 
        protocol="HTTP", 
        port=80, 
        target_type="instance", 
        health_check={
                "path": "/",
                "port": "80",
                "protocol": "HTTP",
                "timeout": 5,
                "interval": 30,
        },
        tags={"Name": "poridhi-exam-tg"}
)

tg_attachment1 = aws.lb.TargetGroupAttachment("poridhi-exam-tg-attachment-1a", 
        target_group_arn=target_group_tg.arn,
        target_id=ec2_instance1.id,
        port=80
)

tg_attachment2 = aws.lb.TargetGroupAttachment("poridhi-exam-tg-attachment-1b", 
        target_group_arn=target_group_tg.arn,
        target_id=ec2_instance2.id,
        port=80
)

# alb 
alb = aws.lb.LoadBalancer("poridhi-exam-alb", 
        load_balancer_type="application",
        security_groups=[security_group.id],
        subnets=[subnet1.id, subnet2.id],
)

listener = aws.lb.Listener("poridhi-exam-listener", 
        load_balancer_arn=alb.arn,
        protocol="HTTP", 
        port=80,
        default_actions=[{
                "type": "forward",
                "target_group_arn": target_group_tg.arn,
        }]
)




# infra 
pulumi.export("vpc_id", vpc.id)
pulumi.export("subnet_1_id", subnet1.id)
pulumi.export("subnet_2_id", subnet2.id)

# netwokring 
pulumi.export("igw_id", igw.id)
pulumi.export("rtb_id", rtb.id)

# ec2
pulumi.export("instance_1_id", ec2_instance1.id)
pulumi.export("instance_2_id", ec2_instance2.id)

# alb
pulumi.export("target_group_id", target_group_tg.id)
pulumi.export("alb.id", alb.id)
pulumi.export("alb_dns_name", alb.dns_name)
pulumi.export("listener_id", listener.id)


""" Key Pair Generation 

A. key pair with aws cli: 
In the below way, the - - query param will save the key in the host and aws cli will be able to access it, 
and just passing the name of the key will be enough in pulumi to create an EC2 instance 
and > will also save it in the file system. 

=> aws ec2 create-key-pair --key-name poridhi-exam-key --query 'KeyMaterial' --output text > poridhi-exam-key.pem

B. using ssh-keygen 

1. ssh-keygen -t rsa -b 2048 -f ~/.ssh/my-key-pair-name
    
    i. -t : the algorithm of key pair 
    ii. -b 2048: the length of the key pair, here 2048 bit which is industry practice 
    iii. -f ~/.ssh/my-key-pair-name: name of the key pair 
2. cat ~/.ssh/my-key-pair-name.pub can be shared 

3. ssh -i ~/.ssh/my-key-pair-name ubuntu@ec2-public-ip : to ssh into server 
"""
