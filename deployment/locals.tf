locals {
  project      = var.project
  prefix       = "${local.project}-${terraform.workspace}"
  azure_region = var.azure_region

  virtual_network_address_space = var.virtual_network_address_space
  aks_version                   = var.aks_version
  aks_nodes_address_cidr        = cidrsubnet(local.virtual_network_address_space, 8, 1)
  aks_vm_size                   = var.aks_vm_size
  aks_node_counts               = var.aks_node_counts
  aks_availability_zones        = var.aks_availability_zones
  aks_api_allow_public          = var.aks_api_allow_public

  aks_api_authorized_ip_ranges = concat(
    var.aks_api_authorized_ip_ranges,
    local.aks_api_allow_public ? ["0.0.0.0/0"] : [],
  )

  default_tags = {
    managedby : "terraform",
    project : local.project,
    environment : terraform.workspace,
  }
}
