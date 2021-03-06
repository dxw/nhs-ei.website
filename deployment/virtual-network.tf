resource "azurerm_virtual_network" "default" {
  name                = "${local.prefix}-default"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  address_space       = [local.virtual_network_address_space]
  tags                = local.default_tags
}

resource "azurerm_subnet" "default_aks_nodes" {
  name                                           = "${local.prefix}-default-aks-nodes"
  virtual_network_name                           = azurerm_virtual_network.default.name
  resource_group_name                            = azurerm_resource_group.default.name
  address_prefixes                               = [local.aks_nodes_address_cidr]
  enforce_private_link_endpoint_network_policies = true
}

resource "azurerm_network_security_group" "default_aks_nodes" {
  name                = "${local.prefix}-default-aks-nodes"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  tags                = local.default_tags
}

resource "azurerm_network_security_rule" "ingress_nginx_load_balancer_http" {
  name                        = "ingress-nginx-load-balancer-http"
  priority                    = 500
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "80"
  source_address_prefix       = "Internet"
  destination_address_prefix  = data.kubernetes_service.ingress_nginx_load_balancer.status[0].load_balancer[0].ingress[0].ip
  resource_group_name         = azurerm_resource_group.default.name
  network_security_group_name = azurerm_network_security_group.default_aks_nodes.name
}

resource "azurerm_network_security_rule" "ingress_nginx_load_balancer_https" {
  name                        = "ingress-nginx-load-balancer-https"
  priority                    = 501
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "443"
  source_address_prefix       = "Internet"
  destination_address_prefix  = data.kubernetes_service.ingress_nginx_load_balancer.status[0].load_balancer[0].ingress[0].ip
  resource_group_name         = azurerm_resource_group.default.name
  network_security_group_name = azurerm_network_security_group.default_aks_nodes.name
}

resource "azurerm_subnet_network_security_group_association" "default_aks_nodes" {
  subnet_id                 = azurerm_subnet.default_aks_nodes.id
  network_security_group_id = azurerm_network_security_group.default_aks_nodes.id
}

resource "azurerm_route_table" "default_aks_nodes" {
  name                          = "${local.prefix}-default-aks-nodes"
  location                      = azurerm_resource_group.default.location
  resource_group_name           = azurerm_resource_group.default.name
  disable_bgp_route_propagation = false
  tags                          = local.default_tags
}

resource "azurerm_subnet_route_table_association" "default_aks_nodes" {
  subnet_id      = azurerm_subnet.default_aks_nodes.id
  route_table_id = azurerm_route_table.default_aks_nodes.id
}

resource "azurerm_private_dns_zone" "default_postgres_private_link" {
  name                = "default-privatelink.postgres.database.azure.com"
  resource_group_name = azurerm_resource_group.default.name
}

resource "azurerm_private_dns_zone_virtual_network_link" "default_postgres_private_link" {
  name                  = "default-postgres-private-link"
  resource_group_name   = azurerm_resource_group.default.name
  private_dns_zone_name = azurerm_private_dns_zone.default_postgres_private_link.name
  virtual_network_id    = azurerm_virtual_network.default.id
}
