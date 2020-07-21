# Cinephile Bot
A Twitter bot that replies to user query tweets and presents them with standard information about films
such as year of release, budget, box office, director(s), actor(s) etc.

*Note: This program uses the TMDb API but is not endorsed or certified by TMDb*

## Techologies Used
TODO: Write technologies used

## Features
TODO: Write list of features and include screenshot

## Requirements
Must have an AWS account and an IAM user with *access key ID* and *secret access key* credentials


## Usage
First, install Ansible and associated dependencies on the control machine
```
sudo apt install python
sudo apt install python-pip
python -m pip install --upgrade pip
pip install boto boto3 ansible
```

Then, generate an RSA public/private key pair for your AWS EC2 instance
```
ssh-keygen -t rsa -b 4096 -f ~/.ssh/my_aws
```

After cloning the directory, store the IAM user credentials securely using ```ansible-vault```
```
cd ansible/
ansible-vault create group_vars/all/pass.yml
ansible-vault edit group_vars/all/pass.yml
```
Example ```pass.yml``` file (*Note: these credentials are examples only*)
```
ec2_access_key: AAAAAAAAAAAAAABBBBBBBBBBBB
ec2_secret_key: afjdfadgf$fgajk5ragesfjgjsfdbtirhf
```

Now, run the playbook to deploy an instance and run a Docker container for the Twitter
bot on your newly provisioned AWS EC2 instance
```
ansible-playbook playbook.yml --ask-vault-pass --tags create_ec2
```

## Issues Faced
TODO: Write issues faced

## License
TODO: Include license