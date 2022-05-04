variable "project" {
  description = "A project name, used to prefix resources launched"
  type        = string
  default     = "nhsei"
}

variable "azure_region" {
  description = "The Azure Region in which all resources in this example should be provisioned"
  type        = string
  default     = "uksouth"
}

variable "virtual_network_address_space" {
  description = "Virtual Network address space CIDR"
  type        = string
  default     = "10.0.0.0/16"
}
