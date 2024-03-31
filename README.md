# AWS_Localstack

Have Localstack running in local cluster. Want to have local Python (i.e. `boto3`) on local machine be able to call the Localstack pod, via the public internet, but restrict access only to authorized individuals. 


### Ideas
- Short-Term: Add a custom HTTP Header check to HTTPRoute. 
- Long-Term: Pay for professional Localstack license and use IAM.


### Problems
1. I want to be able to push my localstack configuration and Python code to public GitHub repos. How can I use a shared secret to secure the traffic is both sets of manifests will be public?

    **A:** Create a K8s Secret ahead of time. Run Python on a machine with `kubectl` access to cluster and run subshell command to retrieve secret. Leverage ArgoCD to modify HTTPRoute **after** deployment to modify the HTTP Header value it looks for to this same secret.