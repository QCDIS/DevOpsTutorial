# DevOpsTutorial
Define a simple REST API with OpenAPI and Swagger, write REST API tests using Postman, develop the application logic, dockerize it and finally perform continuous integration (CI) 

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

Efectivly what is said here is that the "#/definitions/Student" is not defined. 
You can find more about '$ref' here: https://swagger.io/docs/specification/using-ref/

### Define Objects
Scorll down to the bottom of the page and create a new node called 'definitions' and a node 'Student' under that. The code should look like this:
```YAML
definitions:
  Student:
    type: "object"
    properties:
```

#### Exersise 
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

After you fix the error the definition sould looke like this: [swagger.yaml](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/swagger/swagger_3.yaml)


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
The definition sould looke like this: [swagger.yaml](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/swagger/swagger_4.yaml)

### Generate the Server Code 
### Python-flask 

In the swagger editor go to 'Generate Server' and select 'python-flask'


<img src="/images/swagger5.png" alt="swagger"
	title="swagger" width="550"/>
	
Update the requirements files to look like this:

* [requirements.txt](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/python-flask-server-generated/python-flask-server/requirements.txt)
 
* [test-requirements.txt](https://raw.githubusercontent.com/skoulouzis/DevOpsTutorial/req/python-flask-server-generated/python-flask-server/test-requirements.txt)
  

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


