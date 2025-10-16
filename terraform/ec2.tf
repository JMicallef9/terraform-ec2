data "aws_ami" "AMI_al2023" {
	most_recent = true
    owners = ["137112412989"]

	filter {
		name = "name"
		values = ["al2023-ami-2023*-x86_64"]
		}
}

resource "aws_instance" "project_ec2" {
	ami = data.aws_ami.AMI_al2023.id
	instance_type = "t3.micro"

	key_name = "access_key"
	vpc_security_group_ids = [aws_security_group.allow-ssh.id]
    subnet_id = aws_subnet.main.id

	iam_instance_profile = aws_iam_instance_profile.ec2_instance_profile.name

	tags = {
		Name = "project_ec2"
		}
}