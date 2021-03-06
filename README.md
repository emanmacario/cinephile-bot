# 🎥🤖 Cinephile Bot
A Twitter bot that replies to user query tweets and presents them with standard information about films
such as year of release, budget, box office earnings, director(s), actor(s) etc.

<div style="text-align: center">
<img src="./assets/cinephile_bot.JPG" width="500" height="auto" alt="Paths of Glory Tweet">
</div>

## Features
* Uses [Github Actions](https://github.com/features/actions) to build and push my bot's Docker image to [Docker Hub](https://hub.docker.com/) whenever code is pushed into the `master` branch
* Contains an [Ansible](https://www.ansible.com/) playbook to:
    1. Dynamically provision a single AWS EC2 instance (default configuration is `t2.micro` running `Ubuntu Server 18.04 LTS (HVM)` in region `us-east-2`) ([AWS Free Tier](https://aws.amazon.com/free/) eligible)
    2. Install Docker CE on the instance
    3. Pull the Docker image mentioned above, and run a container for it
* Uses [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html) to encrypt my AWS access key and secret key so they are not exposed to the public, but can be stored directly on GitHub
* Uses the [Twitter API](https://developer.twitter.com/en/docs/twitter-api) and the [The Movie Database (TMDb) API v3](https://developers.themoviedb.org/3) to process a user's query (via either tweet or direct message), retrieve movie data, and tweet a response

## Sample Tweet
<div style="text-align: center;">
    <img src="./assets/paths_of_glory.JPG" width="800" height="auto" alt="Paths of Glory Tweet">
</div>

## Sample Direct Message
<div style="text-align: center;">
    <img src="./assets/before_sunset_direct_message.JPG" alt="Paths of Glory Tweet">
</div>

## Requirements
Must have an AWS account and an IAM user with *access key ID* and *secret access key* credentials

## Usage
First, install Ansible and associated dependencies on the control machine
```bash
$ sudo apt install python
$ sudo apt install python-pip
$ python -m pip install --upgrade pip
$ pip install boto boto3 ansible
```

Then, generate an RSA public/private key pair for your AWS EC2 instance
```bash
$ ssh-keygen -t rsa -b 4096 -f ~/.ssh/rsa_aws
```

After cloning the directory, store the IAM user credentials securely using ```ansible-vault```
```bash
$ cd ansible/
$ ansible-vault create group_vars/all/credentials.yml
$ ansible-vault edit group_vars/all/credentials.yml
```
Example ```credentials.yml``` file 
```
aws_access_key: AAAAAAAAAAAAAABBBBBBBBBBBB
aws_secret_key: afjdfadgf$fgajk5ragesfjgjsfdbtirhf
```
**Note**: these credentials are examples only


Now, run the playbook to deploy an instance and run a Docker container for the Twitter
bot on your newly provisioned AWS EC2 instance
```bash
$ ansible-playbook playbook.yml --ask-vault-pass --tags create_ec2
```

## Issues
* Direct messages from the bot may take a while. This is due to a known issue with the Twitter API, where it takes a few minutes for direct messages to register on their backend

## License
MIT © Emmanuel Macario

## Attribution
Created by Emmanuel Macario

**Note**: *This program uses the TMDb API but is not endorsed or certified by TMDb*