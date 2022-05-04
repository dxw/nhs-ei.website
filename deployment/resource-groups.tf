resource "azurerm_resource_group" "default" {
  name     = "${local.prefix}-default"
  location = local.azure_region
  tags     = local.default_tags
}
