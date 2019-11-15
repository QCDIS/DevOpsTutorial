# DevOpsTutorial
Define a simple REST API with OpenAPI and Swagger, write REST API tests using Postman, develop the application logic, dockerize it and finally perform continuous integration (CI) 

## Write the API definitions
To get an understanding of Swagger and OpenAPI you may follow this tutorial till part 5: https://apihandyman.io/writing-openapi-swagger-specification-tutorial-part-1-introduction/. 

### Hands On
Open the swagger editor : http://editor.swagger.io/# .  You should see the ‘Swagger Petstore’ example. 

### Set up example code
<img src="/images/swagger1.png" alt="swagger"
	title="swagger" width="550"/>
	
The existing code is quite complex for a first hands-on. Clear the code:


<img src="/images/swagger2.png" alt="swagger"
	title="swagger" width="550"/>
	
	
<img src="/images/swagger3.png" alt="swagger"
	title="swagger" width="550"/>

Paste the following code into the editor:

```YAML
swagger: "2.0"
info:
  description: "Swagger tutorial"
  version: "1.0.0"
  title: "Swagger tutorial"
basePath: "/service-api"
schemes:
- "http"
paths:
  /student:
    post:
      summary: "Add a new student"
      description: ""
      operationId: "addStudent"
      consumes:
      - "application/json"
      - "application/xml"
      produces:
      - "application/xml"
      - "application/json"
      parameters:
      - in: "body"
        name: "body"
        description: "Student object that needs to be added"
        required: true
        schema:
          $ref: "#/definitions/Student"
      responses:
        405:
          description: "Invalid input"
  /pet/{student_id}:
    get:
      tags:
      - "pet"
      summary: "Find student by ID"
      description: "Returns a single pet"
      operationId: "getStudentById"
      produces:
      - "application/xml"
      - "application/json"
      parameters:
      - name: "student_id"
        in: "path"
        description: "ID of pet to return"
        required: true
        type: "integer"
        format: "int64"
      responses:
        200:
          description: "successful operation"
          schema:
            $ref: "#/definitions/Student"
        400:
          description: "Invalid ID supplied"
        404:
          description: "Pet not found"

```

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
<img src="/images/swagger4.png" alt="swagger"
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
| Property Name        | Type|
| ------------- |:-------------:|
| student_id      | integer (int64 format) |
| first_name      | string      | 
| last_name | string      |


| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |
