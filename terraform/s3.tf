resource "aws_s3_bucket" "ec2_bucket" {
  bucket = "ec2_bucket_2025"

  tags = {
    Name = "ec2_bucket"
  }
}