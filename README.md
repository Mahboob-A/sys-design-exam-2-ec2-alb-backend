# AWS Production Grade Infra Using Pulumi 

This is a Pulumi script to create a scalable and highly available AWS infrastructure for a **Todo app**. It sets up everything needed to run the app in a production-ready environment.

---

## Video Explanation 

To understand the setup better, I recorded where I explain the script and how everything fits together: [Watch Video](https://youtu.be/xFQvzdifPNc?si=gPnmUFVoTA_R2EZ4)

## Pulumi Script 

In the `src/pulumi-iac/` there are a few pulumi sctipts which are developed after a lof of trial errors. But the working script is the `__main__.py` file. 

Here's the: [Final Script](https://github.com/Mahboob-A/sys-design-scalable-aws-env-backend/blob/main/src/pulumi-iac/__main__.py)

## Installation Guide 

I have added instrution how to deploy the Todo app in the environment. Please follow [this](https://github.com/Mahboob-A/sys-design-scalable-aws-env-backend/blob/main/installation.txt) installation guide to run the todo app. You can also watch the video above if you want a glimpse. 

## Client APP 

I have setup a minimal client app in this [repository](https://github.com/Mahboob-A/sys-design-scalable-aws-env-client) to test the todo app backend. 

---

## Overview of the Infrastructure

This setup uses AWS services to ensure the service can handle lots of traffic and run smoothly with minimal downtime. Here's what we are setting up:

1. **VPC (Virtual Private Cloud)**:
    * The VPC where all the resources will live.

2. **Public Subnets** (2 subnets in 2 different availability zones):
    * These are the subnets that will host the **ALB (Application Load Balancer)** and the **Bastion server**. The Bastion server is for SSH access to the private instances. We can also deploy our client app in public subnet, if that is not an issue. 

3. **Private Subnets** (3 subnets in 3 different availability zones):
    * 2 subnets will host the **Django app** instances.
    * 1 subnet will host the **PostgreSQL database**.

4. **Internet Gateway (IGW)**:
    * To allow communicatation between VPC and the internet.

5. **Route Tables** (Public and Private):
    * **Public Route Table** routes the traffic to the internet.
    * **Private Route Table** routes the traffic through a **NAT Gateway** so the private subnets can access the internet.

6. **NAT Gateway**:
    * Allows the private subnet instances to access the internet (outboud traffixc) but keeps them isolated from direct internet access.

7. **Security Groups**:
    * 4 Security Groups are created:
        * One for the Bastion server.
        * One for the ALB (allows HTTP and HTTPS traffic).
        * One for the Django app servers (only allows traffic from ALB and Bastion).
        * One for the PostgreSQL DB (only allows traffic from the Django app servers).

8. **Elastic IP and NAT Gateway**:
    * Elastic IP (EIP) is assigned to the **NAT Gateway** to allow private subnets to access the internet.

9. **Auto Scaling Group (ASG)**:
    * Ensures that the number of Django app instances can grow or shrink based on traffic. It's connected to the ALB to handle requests.

## Components and Explanation

### **VPC (Virtual Private Cloud)**

* Creates a VPC with a CIDR block `10.10.0.0/16`.
* This VPC will contain the public and private subnets.

### **Subnets**:

* **Public Subnets**:
    * Subnet 1 (`10.10.1.0/24`) will host the Bastion server and the client app.
    * Subnet 1 and Subnet 2 (`10.10.2.0/24`) will host the ALB.

* **Private Subnets**:
    * Subnet 1 (`10.10.3.0/24`) and Subnet 2 (`10.10.4.0/24`) will host the Django app.
    * Subnet 3 (`10.10.5.0/24`) will host the PG database.
    * `NOTE:` `The testing todo app backend and pg databases will be depkloyed as docker containers. `

### **Internet Gateway (IGW)**

* An **Internet Gateway** is created and attached to the VPC to allow internet access for the public subnets.

### **Route Tables**:

* **Public Route Table**:
    * Routes all traffic (`0.0.0.0/0`) to the **IGW**.

* **Private Route Table**:
    * Routes traffic through the **NAT Gateway** for the private subnets.

### **NAT Gateway and Elastic IP**:

* **Elastic IP** is assigned to the **NAT Gateway**.
* The **NAT Gateway** is placed in Public Subnet 1 and allows the private subnets to access the internet.

### **Security Groups**:

* **Public Security Group**: Allows SSH (port 22) from anywhere (for Bastion server access).
* **ALB Security Group**: Allows HTTP (port 80) and HTTPS (port 443) traffic from anywhere.
* **Django App Security Group**: Allows traffic only from the ALB (port 80 and 443) and from the Bastion server (port 22).
* **PG DB Security Group**: Allows traffic only from the Django app instances (port 5432) and from the Bastion server (for SSH access).

### **Auto Scaling Group (ASG)**

* The **Auto Scaling Group (ASG)** ensures that thare are always enough instances of the service to handle incoming traffic. It works with the ALB to automatically scale the number of instances based on load.
* The **ALB** routes incoming requests to the available dj app instances in the private sunets, and the ASG ensures that the app instances are running and scaled to handle the traffic.
* It automatically increases or decreases the number of instances depending on the traffics, ensuting cost efficiency. 

### **ALB (Application Load Balancer)**

* The **ALB** is responsible for routing incoming traffic from the internet (HTTP and HTTPS) to the appropriate django app instances.
* It is deployed in the public subnet and forwards the traffic to the instances in the private subnets.
* The ALB works with the **Django App Security Group** to ensure traffic is routed securely to the right app instances.

### **Django Application Instances**

* The **Django app instances** are hosted on EC2 instances within the private subnets. 
* The EC2 instances are launched within the **Auto Scaling Group (ASG)** to ensure that the number of instances adjusts dynamically to the traffic load.
* However, 4 EC2 instancs are out of the scope of **ASG** that are created manually.  
* The instances are associated with the **Django App Security Group**, allowing only traffic from the ALB and Bastion server (for port 22).

### **PostgreSQL Database Instance**

* The **PostgreSQL database instance** is launched in the private subnet.
* It uses the **PostgreSQL DB Security Group**, allowing access only from the Django app instances and the Bastion server (for port 22).
* The database instance is isolated in a private subnet, ensuring security from public internet access.

### **Key Pair**

* A **Key Pair** is created to allow SSH access to the EC2 instances. This key pair is associated with both the Bastion server and the dj app instances for secure access.

## Summary

This Pulumi script provisions a fully managed and scalable infrastructure for hosting a **Production grade aplications**. It ensures secure and optimized communication between all components while being cost-effective and production-ready.

- **VPC** and **subnets** ensure proper isolation and organization of resources.
- **Security Groups** ensure controlled access to resources.
- **Auto Scaling** ensures the app can handle increased traffic.
- **ALB** efficiently distributes traffic across app instances.
- **Private Subnets** and **NAT Gateway** ensure security and proper routing for internal communication.
- **PostgreSQL Database** is secured and hosted within a private subnet.

This infrastructure is designed to be scalable, fault-tolerant, and secure, ready for production use.

## Flow of the App

*   **SSH** from local machine to the **Bastion Server** in the public subnet.
*   From the Bastion server, SSH into the private subnets.
*   The **ALB** (in the public subnet) routes traffic to the Django app instances.
*   The **PostgreSQL DB** is only accessible from the Django app instances (not directly from the internet).
*   The **Auto Scaling Group (ASG)** ensures that the number of Django app instances can scale up or down based on traffic.


## How to Use This Script

1.  Install Pulumi and set up your AWS credentials.
2.  Clone this repo and run the Pulumi script.
3.  It will create all the necessary AWS resources: VPC, subnets, security groups, instances, load balancer, and more.
4. Then you have to follow the `installation.txt` to deploy the todo app in the environment.


## Images 

<br>

![Screenshot from 2024-12-07 13-35-13](https://github.com/user-attachments/assets/970ab8bc-d391-4e97-8127-cc063101f1b1)


![Screenshot from 2024-12-07 10-22-01](https://github.com/user-attachments/assets/ac742cc0-97cf-4765-a80d-08f081183ed0)

![Screenshot from 2024-12-07 13-39-34](https://github.com/user-attachments/assets/631f1e43-0c68-4f16-bd39-5e29c07c039d)

![Screenshot from 2024-12-07 18-34-33](https://github.com/user-attachments/assets/4c0d8a96-2792-4fd8-8d54-293bb2b9c6de)