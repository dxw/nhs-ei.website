resource "random_string" "dbusername" {
  length  = 8
  special = false

  keepers = {
    dbname = "${local.project}-postgresql"
  }
}

resource "random_password" "dbpassword" {
  length           = 20
  special          = true
  override_special = "_%@"

  keepers = {
    dbname = "${local.project}-postgresql"
  }
}

resource "azurerm_postgresql_server" "database" {
  name                = "${local.project}-postgresql"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  tags                = local.default_tags

  sku_name = "GP_Gen5_2"

  storage_mb                   = 5120
  backup_retention_days        = 7
  geo_redundant_backup_enabled = false
  auto_grow_enabled            = true

  administrator_login          = "admin${random_string.dbusername.result}"
  administrator_login_password = random_password.dbpassword.result
  version                      = "11"

  public_network_access_enabled = false
  ssl_enforcement_enabled       = true
}

resource "azurerm_postgresql_database" "db1" {
  name                = "${local.project}-db"
  resource_group_name = azurerm_resource_group.rg.name
  server_name         = azurerm_postgresql_server.database.name
  charset             = "UTF8"
  collation           = "en-GB"
}
