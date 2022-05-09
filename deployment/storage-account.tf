#tfsec:ignore:azure-storage-queue-services-logging-enabled # queue properties cannot be defined when account_kind is BlobStorage
resource "azurerm_storage_account" "default" {
  name                     = lower(replace(local.prefix, "-", ""))
  resource_group_name      = azurerm_resource_group.default.name
  location                 = azurerm_resource_group.default.location
  account_kind             = "BlobStorage"
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
}
