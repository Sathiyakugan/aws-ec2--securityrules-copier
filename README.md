# AWS EC2 security rules Copier
It is a console application to copy the network security rules of a given group of AWS EC2 to a the existing group. 

### Pre Requesties
This application uses Python3. Please make sure you have installed it.
You need to have pip installed along with the Python.

**Boto3 is the  AWS [SDK](https://aws.amazon.com/sdk-for-python/) for Python.** 

please install the Boto3 as per the [documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html#installation). 
```sh
$ pip3 install boto3
```
In the `conf/config.json` replace the placeholders with the  `ACCESS_KEY`, `SECRET_KEY` and the  `REGION_NAME` with your configuration. 
- Note : please folllow these [guidlines](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys) to get the `ACCESS_KEY` and  `SECRET_KEY` .

### Running the Application
1. In the terminal execute the following command:
    ```sh
    $ python3 app.py 
    ```
   Please note that  in some linux versions you can use   `python app.py `  
2. Input the  `existingSecurityGroupId`, `targetSecurityGroupId` when app prompts. 
3. You will see "Success!" Message in the console, If evrythings goes fine. 

License
----
MIT
