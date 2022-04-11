resource "azurerm_resource_group" "rg" {
  name     = "${local.project}-k8s-resources"
  location = var.location
  tags     = local.default_tags
}

# Azure CDN needs a location to store metadata for the profile
# not all regions are supported so we choose one here we know is
resource "azurerm_resource_group" "cdn" {
  name     = "${local.project}-cdn-resources"
  location = "northeurope"
  tags     = local.default_tags
}
