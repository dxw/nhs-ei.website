This documentation covers the deployment process and the creation of infrastructure.

## Deployment

## Azure infrastructure

The infrastructure is managed using [Terraform](https://www.terraform.io/).<br>
The state is stored remotely in encrypted Azure storage.<br>
[Terraform workspaces](https://www.terraform.io/docs/state/workspaces.html) are used to separate environments.

### Creating a new environment

When creating a new staging environment you may wish to build it in the same region as
the current live environment.

#### Configuring the storage backend

The Terraform state is stored remotely in Azure, this allows multiple team members to
make changes and means the state file is backed up. The state file contains
sensitive information so access to it should be restricted, and it should be stored
encrypted at rest.

##### Create a new storage backend

The [Azure tutorial](https://docs.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage) outlines the steps to create a storage account and container for the state file. You will need:

- resource_group_name: The name of the resource group used for the Azure Storage account.
- storage_account_name: The name of the Azure Storage account.
- container_name: The name of the blob container.
- key: The name of the state store file to be created.

##### Create a backend configuration file

Create a new file named `backend.vars` with the following content:

```
resource_group_name  = [the name of the Azure resource group]
storage_account_name = [the name of the Azure Storage account]
container_name       = [the name of the blob container]
key                  = "terraform.tstate"
```

##### Install local software

Install the Azure CLI, Helm and tfenv:
```
$ brew install az helm tfenv
```
##### Log into azure with the Azure CLI

Log in to your account:

```
$ az login
```

Confirm which account you are currently using:

```
$ az account show
```

##### Initialise Terraform

Install the required terraform version:

```
$ tfenv install
```

Initialize Terraform to download the required Terraform modules and configure the remote state backend
to use the settings you specified in the previous step.

From within the `deployment` directory:

`$ terraform init -backend-config=backend.vars`

##### Create a Terraform variables file

Copy the `terraform.tfvars.example` to `terraform.tfvars` and modify the contents as required.
(Or copy from 1Password "NHSEI testing terraform.tfvars")

If you do not wish to create the file, Terraform will ask you to provide the variables
when you run it.

##### Create the infrastructure

Now Terraform has been initialised you can create a workspace. The workspace name is
included in various resources such as the CDN, database, and load balancer.<br>
Do not use a <prefix>-<workspace> combination that already exists unless you know what
you are doing. (You can get a list with `terraform workspace list`)

`$ terraform workspace new staging`

Switch to the new workspace<br>
`$ terraform workspace select staging`

Plan the changes<br>
`$ terraform plan`

(you'll need to have set up Kubernetes credentials, see later.)
(Don't be too surprised if there are changes to helm_release.cron_jobs, .web and .scrapy if there's been releases and you've manually updated the
sha to the most recent version -- Terraform doesn't know about the changes that Github Actions have caused.)

Terraform will ask you to provide any variables not specified in an `*.auto.tfvars` file.
Now you can run:

`$ terraform apply`

If everything looks good, answer `yes` and wait for the new infrastructure to be created.

#### Terraform variables for infrastructures already launched

There are 2 terraform variables that needs to be changed often, the `web_image_tag` and the `scrapy_image_tag`

This is because the image tags are updated automatically when deployed via GitHub actions

We need to get the value of these before running `terraform apply`, otherwise we risk rolling back, or deploying latest when it's not ready

To get the image tag values, first list the helm releases:

```
helm list -A
```

From that list, find the namespace of the helm release (the second column), and its name (the first), and run the following to get the values:

```
helm get values --namespace <NAMESPACE> <NAME>
```

This will output all the values associated with the release, eg:

```
USER-SUPPLIED VALUES:
environment:
  # environment variables
image:
  tag: sha-1234567890123456789212345678931234567894
# redacted ...
```

Copy the image tag into the terraform.tfvars file (including the 'sha-')

The rest of the values are stored in 1Password.

You should update these variables in terraform.tfvars before running, since they'll roll back to the version
you've specified if there's been any changes to main.

#### Adding environment variables to the services

There are 2 terraform variables (maps) that can be updated to add, change or remove environment variables

`web_environment_variables` and `scrapy_environment_variables`

To add an environment variable, just append it to the map, eg:

```
web_environment_variables = {
  EXISTING_ENVAR = "foo"
  NEW_ENVAR      = "bar"
}
```

Then run `terraform apply`

This will apply to the service, and cron job

Note: Take care not to accidently overwrite environment variables that are automatically added (eg. the `DATABASE_URL`). These can be found in the `kubernetes-service-web.tf` and `kubernetes-service-scrapy.tf` files. But if you wish, you can overwrite them, as the variable supplied environment variables are added after the ones automatically added. (Note: These will show as differences on the terraform plan, because terraform doesn't know that Github Actions have been automatically updating the server.)

#### Connecting to the Kubernetes cluster

Install kubectl (The kubernetes cli):

```
$ brew install kubectl
```

Configure kubectl to connect to the Kubernetes cluster:

```
$ az aks get-credentials --resource-group <ResourceGroup> --name <AKSCluster>
```

(The AKSCluster is the name of the Kubernetes service in Azure and the resource group is its resource group, listed top-left)

You should be able to run `kubectl` commands normally, eg:

```
$ kubectl get pods -A
```

#### View the status of Scrapy

Scrapy isn't publically accessable, so we need to use kubectl to port-forward from our local machines to the running service

List the services to find the name of the scrapy service:

```
$ kubectl get services --namespace scrapy
```

Port forward to 8001:

```
$ kubectl port-forward --namespace scrapy service/<ScrapyServiceName> 8001:8001
```

Open http://localhost:8001 in your browser

#### Accessing containers

List the pods to find the one you wish to connect to:

```
$ kubectl get pods -A
```

or also specify the namespace to filter pods:

```
$ kubectl get pods --namespace web
```

Connect to one of the pods returned:

```
$ kubectl exec -ti --namespace web <PodName> -- /bin/bash
```

#### Accessing Postgres

The postgres database can be accessed via the web service or scrapy service.

Connect to one of the containers as described above.

To run a shell in postgres, run:

```
./manage.py dbshell
```

#### Viewing logs

The logs are accessible via the Azure portal

Log in, and navigate to the Kubernetes service console

Select the required kubernetes service

Select 'Services and ingresses'

Select either the web or scrapy service

Select 'Pods'

Select the Pod in the list

Select 'Live logs'

Select the pod from the drop down

You can also select the link 'View in Log Analytics' to view historical logs

#### Generating Azure Credentials for GitHub actions

GitHub actions requires access to AKS to do a helm release

To generate these for a new environment, run:

```
az ad sp create-for-rbac \
  -n "nhsei-<ENVIRONMENT>-default-resources-authentication" \
  --role Contributor \
  --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/nhsei-<ENVIRONMENT>-default \
  --sdk-auth
```

The ENVIRONMENT is the Terraform workspace, and you can find the SUBSCRIPTION_ID in the Azure portal under the Subscription Service)

Format the output into a single line before adding to GitHub actions

##### Show Cronjobs

`kubectl get cronjobs -A`

(The cronjobs are in deployment/kubernetes-cron-jobs.tf)
