terraform {
  required_version = ">= 1.1.8"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.2.0"
    }
    helm       = ">= 2.5.1"
    kubernetes = ">= 2.10.0"
  }
}
