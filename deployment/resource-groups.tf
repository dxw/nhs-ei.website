resource "azurerm_resource_group" "default" {
  name     = "${local.prefix}-default"
  location = local.azure_region
  tags     = local.default_tags
}

# Some resources can only be launched in North Europe (eg. CDN resources)
# This resource group os for those resources
resource "azurerm_resource_group" "northeurope" {
  name     = "${local.prefix}-northeurope"
  location = "northeurope"
  tags     = local.default_tags
}
