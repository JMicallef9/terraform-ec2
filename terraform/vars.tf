variable "bucket_name" {
    description = "S3 bucket name"
    type = string
}

variable "local_filepath" {
    description = "Local file to upload before EC2 runs"
    type = string
}

variable "input_key" {
    description = "S3 key for uploaded input file"
    type = string
}

variable "output_key" {
    description = "S3 key for processed CSV output"
    type = string
    default = "output/result.csv"
}