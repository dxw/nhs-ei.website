data "azurerm_container_registry" "web" {
  name                = local.acr_options["name"]
  resource_group_name = local.acr_options["resource_group"]
}
