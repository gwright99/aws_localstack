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
6. Function `get_localstack_http_secret` in `apps/create_bucket/src/config/getsetvalues.py` has logic to grab K8s secret value (via `kubectl`, which is present on the remote development system).
7. Functions `_add_header` and `augment_aws_client_with_http_header` in `apps/create_bucket/src/utils/localstack.py` are used to dynamically patch and `boto3` client to automagically send the extra HTTP header requires to satisfy the API Gateway security check.


### Development (Intellisense & AutoComplete)

Total PITA to get this working. Solution(s):

1. Finding packages:

    1. Use `venv` (_Yes it's not as cool as new packages like poetry, but I had enough problems already I didn't need to make this any harder than necessary_). Command `python -m venv venv`

    2. Activate venv (`source venv/bin/activate` and install packages. Eg. `boto3-stubs[ec2,s3,rds,dynamodb,WHATEVER]`

    3. Update VSCode `settings.json` with at least these:
        ```json
        {
            "python.languageServer": "Pylance",

            "python.analysis.extraPaths": [
                "/home/ubuntu/localstack/venv/lib/python3.10/site-packages",
                // To get Pylance to STFU about missing imports
                "/home/ubuntu/localstack/apps/create_bucket/src"
            ],
            "python.autoComplete.extraPaths": [
                "/home/ubuntu/localstack/venv/lib/python3.10/site-packages",
            ]
        }
        ```

2. Getting auto-completion to work

    1. In `.py` file, import the service client. Eg. `from mypy_boto3_s3.client import S3Client`.
    
    2. Annotate your client variable with the type hint. This should allow VScode to start being helpful re: object attributes/methods/return types.
 

### Testing

Decided to go with a classic `src` and `tests` peer folder structure split to separate app logic from testing logic, and use **pytest** as the testing framework. 

Like every attempt to use pytest in the past, with this sort of structure, ran into a plethora of IDE problems (import failures, autocompletion failures, cant-find-test failures, etc). Took the following steps to get things working.

1. `echo PYTHONDONTWRITEBYTECODE=1 >> ~/.basrhc`
    Got tired of `__pycache` folder cluttering up the project. Originally I tried to stop this in the `.py` files themselves but results were inconsistent: (_according to [StackOverflow](https://stackoverflow.com/questions/50752302/python3-pycache-generating-even-if-pythondontwritebytecode-1) this may be due to `python.testing.pytestEnabled` being active, causing VSCode to ignore. Dunno.)

    ```python
    import sys
    sys.dont_write_bytecode = True
    ```

2. Implemented solution documented by Mike Rodent on the SO article: [pytest cannot import module while python can](https://stackoverflow.com/questions/41748464/pytest-cannot-import-module-while-python-can) re how to get tests to run and resolved in a project structure with peered `src` and `tests` folders. Some users have said his appraoch is incorrect, but I found it was the only way to get thing working properly for me too. TLDR:
    - Add `conftest.py` as another peer to `src` and `tests`
    - Add the following code at the top of `conftest.py` so it can find the actual `src` files:

        ```python
        import sys
        import pathlib

        this_file_path = pathlib.Path(__file__)
        src_core_dir_path_str = str(this_file_path.parent.joinpath('src'))
        sys.path.insert(0, src_core_dir_path_str)
        ```

3. Created a toy implementation of session/module/function-level fixtures to setup and teardown S3 buckets/files in Localstack (works). 

    1. See `app/create_bucket/tests/test_s3.py`.
        
        Fixtures are currently located in the same module where the tests are. Some (like `s3_client` generation) should probably be moved upstream in the project for better reuse.

4. Manipulated path in actual test files so they could be run directly via `python -i <PATH/TO/TESTFILE>`.

    Sometimes it's helpful to open an interactive session to troubleshoot a particular function. To avoid import errors, I added the following to the top of the test `.py` files. **NOTE:**_Since path is relative, you need to run from the same folder where the file is located (i.e. `cd app/create_bucket/tests && python3 -i test_s3.py` NOT `python3 <PATH>/test_s3.py`).

    ```python
    import sys
    sys.path.insert(0, '../src')
    ```

5. Run tests:

    ```bash
    # I originally had to run pytest as a python module or else imports broke. With the conftest.py path manipulation, both options appeare via now.

    $ cd ~/localstack/apps/create_bucket
    $ python -m pytest -s -v 
    # OR
    $ pytest -s -v
    ```