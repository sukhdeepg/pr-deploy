# PR-DEPLOY

Our broad idea was to automatically host a static website on a webserver when a pull request is created. So for example, if on the repo 'my-dog-website' a pull request is created, a comment will be added to the pull request specifying the link of where the app is deployed. Example - **my-dog-website.prdeploy.xyz**.

## Work Done:
1. Set up an nginx server on a Digital Ocean droplet and configured the server to serve requests from any subdomain.
2. Set up the DNS to route traffic from all the subdomains to our server. 
3. Set up a Github app that will trigger a webhook on a PR request. 
4. A flask webapp that will listen for the PR request event. It will then clone the repo, build it and deploy it. 

## In Progress:
1. Configure the nginx server to run the webapp that is called when a PR is raised and serve the static files simultaneously on the same droplet.
2. Instead of relying on Github PR webhook, create a general API that will receive the repo name, branch name and the clone URL. The handler would then clone, build and deploy.

We plan to complete and polish the project in the next few days.

We thank Anand Chitipothu for guiding us through the project.
