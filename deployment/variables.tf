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

variable "custom_apex_domain" {
  description = "Custom apex domain. This is the apex domain that will be used to genereate TLS certificates for the ingress. A DNS record must be created for each environment once the ingress has been launched - eg. <project>-ingress.<terraform-workspace>.<custom_apex_domain>"
  type        = string
  default     = ""
}

variable "cdn_hostname" {
  description = "CDN Hostname"
  type        = string
  default     = ""
}

variable "letsencrypt_email" {
  description = "Letsencrypt email"
  type        = string
  default     = ""
}

variable "letsencrypt_server" {
  description = "Letsencrypt server"
  type        = string
  default     = "https://acme-v02.api.letsencrypt.org/directory"
}

variable "virtual_network_address_space" {
  description = "Virtual Network address space CIDR"
  type        = string
  default     = "10.0.0.0/16"
}

variable "acr_options" {
  description = "Name and Resource group of existing ACR containing the web image"
  type        = map(string)
  default = {
    name           = "nhseiwebsite"
    resource_group = "nhsei-website-container"
  }
}

variable "web_image_tag" {
  description = "Tag of web image to deploy"
  type        = string
}

variable "web_environment_variables" {
  description = "Web environment variables"
  type        = map(string)
  default     = {}
}

variable "scrapy_image_tag" {
  description = "Tag of scrapy image to deploy"
  type        = string
}

variable "scrapy_environment_variables" {
  description = "Web environment variables"
  type        = map(string)
  default     = {}
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
