terraform {
	required_providers {
		aws = {
			source = "hashicorp/aws"
			version = "~>5.0"
			}
		}
}

# configuring AWS provider
provider "aws" {
	region = "eu-west-2"
}