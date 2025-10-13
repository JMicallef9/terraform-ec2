data "aws_ami" "AMI_al2023" {
	most_recent = true
	filter {
		name = "name"
		values = ["al2023-ami-2023*-x86_64"]
		}
}

resource "aws_instance" "access_all_areas" {
	ami = data.aws_ami.AMI_al2023.id
	instance_type = "t2.micro"

	key_name = "access_key"
	vpc_security_group_ids = [aws_security_group.allow-ssh.id]
    subnet_id = aws_subnet.main.id
	tags = {
		Name = "access_all_areas"
		}
}