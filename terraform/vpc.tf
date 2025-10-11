resource "aws_security_group" "allow-ssh" {
	name = "allow_ssh"
    description = "Allow SSH inbound traffic"
    vpc_id = aws_vpc.main.id
	
	ingress {
        from_port = 22
		to_port = 22
		protocol = "tcp"
		cidr_blocks = ["0.0.0.0/0"] 
    }

    egress {
        from_port = 0
		to_port = 0
		protocol = "-1"
		cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "my-vpc"
  }
}