# AWS_Localstack

Have Localstack running in local cluster. Want to have local Python (i.e. `boto3`) on local machine be able to call the Localstack pod, via the public internet, but restrict access only to authorized individuals. 


### Ideas
- Short-Term: Add a custom HTTP Header check to HTTPRoute. 
- Long-Term: Pay for professional Localstack license and use IAM.


### Problems
1. I want to be able to push my localstack configuration and Python code to public GitHub repos. How can I use a shared secret to secure the traffic is both sets of manifests will be public?

    **A:** Create a K8s Secret ahead of time. Run Python on a machine with `kubectl` access to cluster and run subshell command to retrieve secret. Leverage ArgoCD to modify HTTPRoute **after** deployment to modify the HTTP Header value it looks for to this same secret.


### Structure

1. Want to point to localstack but be able to pivot quickly to real AWS if necessary. Structure code in a way to be able to modify target quickly.

2. Design heavily influenced by [https://pypi.org/project/boto3-stubs/](https://pypi.org/project/boto3-stubs/) implementation suggestion (for minimal code and functional auto-completion).


### Setup

1. Get ArgoCD app running.
2. `cd ~/localstack && source venv/bin/activate`
3. `pip install -r apps/core/requirements.txt`
4. Update `apps/testing/src/config/getsetvalues.py`
5. Generate a bespoke shared password: `k get secret -n localstack header-secret -o json | jq --arg header "$(echo YOUR_BESPOKE_PASSWORD | base64 -w 0)" '.data["header"]=$header' | kubectl apply -f - `
5. `python3 apps/testing/src/testing.py`