resource "random_password" "default_postgresql_password" {
  length           = 20
  special          = true
  override_special = "_%@"
}

resource "azurerm_postgresql_server" "default" {
  name                = "${local.prefix}-default"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  tags                = local.default_tags

  sku_name = "GP_Gen5_2"

  storage_mb                   = 20480
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = replace(local.prefix, "-", "_")
  administrator_login_password = random_password.default_postgresql_password.result
  version                      = "11"

  public_network_access_enabled    = false
  ssl_enforcement_enabled          = true
  ssl_minimal_tls_version_enforced = "TLS1_2"
}

resource "azurerm_postgresql_configuration" "default_log_connections" {
  name                = "log_connections"
  resource_group_name = azurerm_resource_group.default.name
  server_name         = azurerm_postgresql_server.default.name
  value               = "on"
}

resource "azurerm_postgresql_configuration" "default_connection_throttling" {
  name                = "connection_throttling"
  resource_group_name = azurerm_resource_group.default.name
  server_name         = azurerm_postgresql_server.default.name
  value               = "on"
}

resource "azurerm_postgresql_configuration" "default_log_checkoints" {
  name                = "log_checkpoints"
  resource_group_name = azurerm_resource_group.default.name
  server_name         = azurerm_postgresql_server.default.name
  value               = "on"
}

resource "azurerm_postgresql_database" "default_web" {
  name                = "${replace(local.prefix, "-", "_")}_web"
  resource_group_name = azurerm_resource_group.default.name
  server_name         = azurerm_postgresql_server.default.name
  charset             = "UTF8"
  collation           = "en-GB"
}

resource "azurerm_postgresql_database" "default_scrapy" {
  name                = "${replace(local.prefix, "-", "_")}_scrapy"
  resource_group_name = azurerm_resource_group.default.name
  server_name         = azurerm_postgresql_server.default.name
  charset             = "UTF8"
  collation           = "en-GB"
}

resource "azurerm_private_endpoint" "default_aks_nodes_default_postgresql" {
  name                = "${local.prefix}-default-aks-nodes-default-postgresql-private-endpoint"
  location            = azurerm_resource_group.default.location
  resource_group_name = azurerm_resource_group.default.name
  subnet_id           = azurerm_subnet.default_aks_nodes.id

  private_service_connection {
    name                           = "${local.prefix}-default-aks-nodes-default-postgresql-private-service-connection"
    private_connection_resource_id = azurerm_postgresql_server.default.id
    subresource_names              = ["postgresqlServer"]
    is_manual_connection           = false
  }
}

resource "azurerm_private_dns_a_record" "default_postgres" {
  name                = local.prefix
  zone_name           = azurerm_private_dns_zone.default_postgres_private_link.name
  resource_group_name = azurerm_resource_group.default.name
  ttl                 = 300
  records             = [azurerm_private_endpoint.default_aks_nodes_default_postgresql.private_service_connection.0.private_ip_address]
}
