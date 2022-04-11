resource "azurerm_cdn_profile" "cdn" {
  name                = "${local.project}-cdn"
  location            = azurerm_resource_group.cdn.location
  resource_group_name = azurerm_resource_group.cdn.name
  sku                 = "Standard_Microsoft"
  tags                = local.default_tags
}

resource "azurerm_cdn_endpoint" "endpoint" {
  name                = "${local.project}-cdn-endpoint"
  location            = azurerm_cdn_profile.cdn.location
  resource_group_name = azurerm_cdn_profile.cdn.resource_group_name
  profile_name        = azurerm_cdn_profile.cdn.name
  tags                = local.default_tags

  origin {
    name      = "${local.project}-ingress-load-balancer"
    host_name = "${local.project}.${azurerm_kubernetes_cluster.cluster.location}.cloudapp.azure.com"
  }
  origin_host_header = "www.england.nhs.uk"
}
