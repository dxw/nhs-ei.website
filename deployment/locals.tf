locals {
  project = "${var.prefix}-${terraform.workspace}"
  default_tags = {
    prefix : var.prefix,
    managedby : "terraform",
    project : "nhsei-website",
    environment : terraform.workspace,
  }
}
