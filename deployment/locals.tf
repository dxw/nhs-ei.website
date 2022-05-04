locals {
  project      = var.project
  prefix       = "${local.project}-${terraform.workspace}"
  azure_region = var.azure_region

  virtual_network_address_space = var.virtual_network_address_space
  aks_nodes_address_cidr        = cidrsubnet(local.virtual_network_address_space, 8, 1)

  default_tags = {
    managedby : "terraform",
    project : local.project,
    environment : terraform.workspace,
  }
}
