# DevOpsTutorial
Define a simple REST API with OpenAPI and Swagger, write REST API tests using Postman, develop the application logic, dockerize it and finally perform continuous integration (CI) 

## Prerequisites
* git and Github/Gitlab/Bitbuacket account 
* Python3.7 
* Docker and dockerhub account 

## Write the API definitions
To get an understanding of Swagger and OpenAPI you may follow this tutorial till part 5: https://apihandyman.io/writing-openapi-swagger-specification-tutorial-part-1-introduction/. 



### Hands On
Open the swagger editor : http://editor.swagger.io/# .  You should see the ‘Swagger Petstore’ example. 

### Set up example code
<img src="https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/images/swagger1.png" alt="swagger"
	title="swagger" width="550"/>
	
The existing code is quite complex for a first hands-on. Clear the code:


<img src="https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/images/swagger2.png" alt="swagger"
	title="swagger" width="550"/>
	
	
<img src="https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/images/swagger3.png" alt="swagger"
	title="swagger" width="550"/>

Paste the following code into the editor:
[swagger.yaml](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/swagger/swagger_1.yaml)

You will notice that the editor throws two errors: 
```
Errors 
Semantic error at paths./student.post.parameters.0.schema.$ref
$refs must reference a valid location in the document
Jump to line 27
Semantic error at paths./pet/{student_id}.get.responses.200.schema.$ref
$refs must reference a valid location in the document
Jump to line 52
```
<img src="https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/images/swagger4.png" alt="swagger"
	title="swagger" width="550"/>

Effectively what is said here is that the "#/definitions/Student" is not defined. 
You can find more about '$ref' here: https://swagger.io/docs/specification/using-ref/

### Define Objects
Scroll down to the bottom of the page and create a new node called 'definitions' and a node 'Student' under that. The code should look like this:
```YAML
definitions:
  Student:
    type: "object"
    properties:
```

#### Exercise 
Define the Student's object properties. The properties to set are:


| Property Name | Type          		|
| ------------- |:-------------:		| 
| student_id    | integer (int64 format)	| 
| first_name    | string			|  
| last_name     | string			| 
| grades	| map				| 

You can find details about data models here: https://swagger.io/docs/specification/data-models/

The definition sould looke like this: [swagger.yaml](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/swagger/swagger_2.yaml)

### Add Delete method
The API definition at the moment only has 'GET' and 'POST' methdos. We will add a 'DELETE' method 
Before the 'definitions' node add the following:
```YAML
    delete:
      description: ""
      operationId: "deleteStudent"
      produces:
      - "application/xml"
      - "application/json"   
      responses:
        200:
          description: "successful operation"
          schema:
            $ref: "#/definitions/Student"
        400:
          description: "Invalid ID supplied"
        404:
          description: "student not found"  
```
You will notice that the editor is throwing an error:
```
Errors
Hide
 
Semantic error at paths./pet/{student_id}
Declared path parameter "student_id" needs to be defined within every operation in the path (missing in "delete"), or moved to the path-level parameters object
Jump to line 31
```
#### Exersise 
Fix the 'DELETE' method to remove this error

After you fix the error the definition should look like this: [swagger.yaml](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/swagger/swagger_3.yaml)


### Add Query Parametres to Grt
We will update the get method to include query parametres
In the 'parameters' node add the following:
```YAML
      - name: "subject"
        in: "query"
        description: "The subject name"
        required: false
        type: "string"  
```
The definition should look like this: [swagger.yaml](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/swagger/swagger_4.yaml)

### Generate the Server Code 
### Python-flask 

In the swagger editor go to 'Generate Server' and select 'python-flask'


<img src="/images/swagger5.png" alt="swagger"
	title="swagger" width="550"/>
	
Update the requirements files to look like this:

* [requirements.txt](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/python-flask-server-generated/python-flask-server/requirements.txt)
 
* [test-requirements.txt](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/python-flask-server-generated/python-flask-server/test-requirements.txt)

Also the generated code comes with a bug in 'util.py' in the '_deserialize' method. Replace the code for the  '_deserialize' method with this:
```Python
def _deserialize(data, klass):
    """Deserializes dict, list, str into an object.
    :param data: dict, list or str.
    :param klass: class literal, or string of class name.
    :return: object.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif hasattr(klass, '__origin__'):
        if klass.__origin__ == list:
            return _deserialize_list(data, klass.__args__[0])
        if klass.__origin__ == dict:
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)
```
  

#### Commit Code to Git
Go to the directory of the code and add, commit and push the  code: 
```
git add .
git commit -m "<your message here>"
git push
```
More information on git can be found here: https://www.tutorialspoint.com/git/index.htm


#### Create Python Virtual Environment
Go to your local folder in 'python-flask-server-generated/python-flask-server' and create a new Python Virtual Environment:
```
python3 -m venv venv
```
More infromation on Python Virtual Environment can be found here: https://docs.python.org/3/tutorial/venv.html

#### Add Edit .gitignore file 
Beacuse you don't want to push the entire venv folder in git add/edit the '.gitignore' file to look like this:

[.gitignore](https://github.com/skoulouzis/DevOpsTutorial/blob/req/python-flask-server-generated/.gitignore)

#### Install Requirements and Run
Go to 'python-flask-server-generated/python-flask-server' and install the project requirements :
```
./venv/bin/pip3 install --no-cache-dir -r requirements.txt
```
and the test requirements:
```
./venv/bin/pip3 install --no-cache-dir -r python-flask-server/test-requirements.txt
```
Go to python-flask-server-generated/python-flask-server
Run the service:
```
./venv/bin/python3 -m swagger_server
```
Go to: http://localhost:8080/service-api/ui/ 
You should see something like this:
<img src="https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/images/swagger-ui.png" alt="swagger"
	title="swagger" width="550"/>
	

### Write Unit Tests
### Python
The code generated has also created a TestCase. Go to 'python-flask-server-generated/python-flask-server/swagger_server/test' and open the 'test_default_controller.py' file. 
There you can add the test 'test_add_student'. Here is the [test_default_controller.py](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/tests/python-flask-server-generated/python-flask-server/swagger_server/test/test_default_controller.py)

#### Exersise 
Write the 'test_delete_student' test.
After you wrote the test it should look like this: [test_default_controller.py](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/test_delete/python-flask-server-generated/python-flask-server/swagger_server/test/test_default_controller.py)

After you are done commit the code.

### Develop The Application Logic 
Write the code for the get, delete and put methods. 

In general it is a good idea to write application using layred architecture. By segregating an application into tiers, a developer can modifying or adding a layer, instead of reworking the entire application. 

This is why we should create a new package in the code called 'service' and a python file named 'student_service.py'. Here is a template of such a file: [student_service.py](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/student_service/python-flask-server-generated/python-flask-server/swagger_server/service/student_service.py)

Now the controller just needs to call the service's methods: [default_controller.py](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/student_service/python-flask-server-generated/python-flask-server/swagger_server/controllers/default_controller.py)


After you are done commit the code.

#### Create a Board
All code repositories have some kind of board to manage projects. In github Got to 'Projects' and create one. Next go to 'issues' and create three issues: 'develop add_student', 'develop delete_student', 'develop get_student_by_id'. Assign each issue to one person and go back to the project you just created and add the issues to the board in the 'To do' column. 


#### Create a branch and Merage 
Check out the master branch. 
```
git checkout master
```
Create the issue branch 
```
git checkout -b iss3
```

Develop the code and commit to your branch 
```
git add .
git commit -a -m 'added a get_student_by_id [issue 3]'
git push
```
As soon as you have fixed the  issue assigned to you ask for a pull request 


# Continues Testing and Integration 
## Jenkins File 
Material on Jenkinsfile and Jenkins pipeline can be found here: https://jenkins.io/doc/book/pipeline/jenkinsfile/

[Jenkinsfile](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/CI-CD/python-flask-server-generated/python-flask-server/Jenkinsfile)

## Docker
[Dockerfile](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/CI-CD/python-flask-server-generated/python-flask-server/Dockerfile)


