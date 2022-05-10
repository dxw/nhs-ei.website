resource "kubernetes_namespace" "cron_jobs" {
  metadata {
    name = "cron-jobs"
  }
}

resource "helm_release" "cron_jobs" {
  name      = "${local.prefix}-cron-jobs"
  chart     = "./helm/nhsei-cron-jobs"
  namespace = kubernetes_namespace.cron_jobs.metadata.0.name

  # scrapy run all imports
  set {
    name  = "jobs.scrapy-run-all-imports.image.tag"
    value = local.scrapy_image_tag
  }

  set {
    name  = "jobs.scrapy-run-all-imports.env.DATABASE_URL"
    value = local.default_postgres_scrapy_db_url
  }

  dynamic "set" {
    for_each = local.scrapy_environment_variables
    content {
      name  = "jobs.scrapy-run-all-imports.env.${set.key}"
      value = set.value
    }
  }

  set {
    name  = "jobs.scrapy-run-all-imports.schedule"
    value = "0 18 * * *"
  }

  set {
    name  = "jobs.scrapy-run-all-imports.command[0]"
    value = "/bin/bash"
  }

  set {
    name  = "jobs.scrapy-run-all-imports.args[0]"
    value = "-c"
  }

  set {
    name  = "jobs.scrapy-run-all-imports.args[1]"
    value = "cd ./bin && ./run_all_imports.sh"
  }

  # website publish scheduled pages
  set {
    name  = "jobs.publish-scheduled-pages.image.tag"
    value = local.web_image_tag
  }

  set {
    name  = "jobs.publish-scheduled-pages.schedule"
    value = "0 * * * *"
  }

  set {
    name  = "jobs.publish-scheduled-pages.command[0]"
    value = "/bin/bash"
  }

  set {
    name  = "jobs.publish-scheduled-pages.args[0]"
    value = "-c"
  }

  set {
    name  = "jobs.publish-scheduled-pages.args[1]"
    value = "./manage.py publish_scheduled_pages"
  }

  set {
    name  = "jobs.publish-scheduled-pages.env.SCRAPY_ENDPOINT"
    value = "http://${data.kubernetes_service.scrapy.spec.0.cluster_ip}:8001"
  }

  set {
    name  = "jobs.publish-scheduled-pages.env.DATABASE_URL"
    value = local.default_postgres_web_db_url
  }

  set {
    name  = "jobs.publish-scheduled-pages.env.WAGTAIL_SEARCH_URLS"
    value = "http://${data.kubernetes_service.elasticsearch.spec.0.cluster_ip}:9200"
  }

  dynamic "set" {
    for_each = local.web_environment_variables
    content {
      name  = "jobs.publish-scheduled-pages.env.${set.key}"
      value = set.value
    }
  }
}
