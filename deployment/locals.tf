locals {
  project      = var.project
  prefix       = "${local.project}-${terraform.workspace}"
  azure_region = var.azure_region

  custom_apex_domain = var.custom_apex_domain
  letsencrypt_email  = var.letsencrypt_email
  letsencrypt_server = var.letsencrypt_server

  virtual_network_address_space = var.virtual_network_address_space
  acr_options                   = var.acr_options
  web_image_tag                 = var.web_image_tag
  web_replica_count             = var.web_replica_count
  web_environment_variables     = var.web_environment_variables
  scrapy_image_tag              = var.scrapy_image_tag
  scrapy_replica_count          = var.scrapy_replica_count
  scrapy_environment_variables  = var.scrapy_environment_variables
  aks_version                   = var.aks_version
  aks_nodes_address_cidr        = cidrsubnet(local.virtual_network_address_space, 8, 1)
  aks_vm_size                   = var.aks_vm_size
  aks_node_counts               = var.aks_node_counts
  aks_availability_zones        = var.aks_availability_zones
  aks_api_allow_public          = var.aks_api_allow_public

  aks_api_authorized_ip_ranges = concat(
    var.aks_api_authorized_ip_ranges,
    local.aks_api_allow_public ? ["0.0.0.0/0"] : [],
  )

  default_postgres_username      = "${azurerm_postgresql_server.default.administrator_login}@${azurerm_postgresql_server.default.name}"
  default_postgres_password      = azurerm_postgresql_server.default.administrator_login_password
  default_postgres_host          = trim(azurerm_private_dns_a_record.default_postgres.fqdn, ".")
  default_postgres_port          = "5432"
  default_postgres_web_db        = azurerm_postgresql_database.default_web.name
  default_postgres_web_db_url    = "psql://${local.default_postgres_username}:${local.default_postgres_password}@${local.default_postgres_host}:${local.default_postgres_port}/${local.default_postgres_web_db}?sslmode=require"
  default_postgres_scrapy_db     = azurerm_postgresql_database.default_scrapy.name
  default_postgres_scrapy_db_url = "psql://${local.default_postgres_username}:${local.default_postgres_password}@${local.default_postgres_host}:${local.default_postgres_port}/${local.default_postgres_scrapy_db}?sslmode=require"

  ingress_hostname     = "${local.prefix}-ingress.${local.azure_region}.cloudapp.azure.com"
  cdn_origin_host_name = local.custom_apex_domain == "" ? local.ingress_hostname : "${local.project}-ingress.${terraform.workspace}.${local.custom_apex_domain}"
  cdn_hostname         = var.cdn_hostname

  default_tags = {
    managedby : "terraform",
    project : local.project,
    environment : terraform.workspace,
  }
}
