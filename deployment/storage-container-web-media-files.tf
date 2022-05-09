#tfsec:ignore:azure-storage-no-public-access # Allow public read
resource "azurerm_storage_container" "web_media" {
  name                  = "web-media"
  storage_account_name  = azurerm_storage_account.default.name
  container_access_type = "blob"
}
