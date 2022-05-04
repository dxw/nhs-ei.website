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

variable "aks_version" {
  description = "Azure Kubenetes Service version"
  type        = string
  default     = "1.21.9"
}

variable "aks_vm_size" {
  description = "Azure Kubenetes Service vm size"
  type        = string
  default     = "Standard_DS2_v2"
}

variable "aks_node_counts" {
  description = "Azure Kubenetes Service node counts"
  type        = map(number)
  default = {
    count = 2
    min   = 1
    max   = 4
  }
}

variable "aks_availability_zones" {
  description = "Azure Kubenetes Service availability zones"
  type        = list(number)
  default     = [1, 2, 3]
}

variable "aks_api_authorized_ip_ranges" {
  description = "IP ranges allowed to access the Azure Kubenetes Service API Server"
  type        = list(string)
  default     = []
}

variable "aks_api_allow_public" {
  description = "Allow 0.0.0.0/0 access to the Kubenetes Service API Server"
  type        = bool
  default     = true
}
