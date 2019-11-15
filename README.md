# DevOpsTutorial
Define a simple REST API with OpenAPI and Swagger, write REST API tests using Postman, develop the application logic, dockerize it and finally perform continuous integration (CI) 

## Write the API definitions
To get an understanding of Swagger and OpenAPI you may follow this tutorial till part 5: https://apihandyman.io/writing-openapi-swagger-specification-tutorial-part-1-introduction/. 

### Hands On
Open the swagger editor : http://editor.swagger.io/# .  You should see the ‘Swagger Petstore’ example. 

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
definitions:
  Student:
    type: "object"
    properties:
      student_id:
        type: "integer"
        format: "int64"

```



