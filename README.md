

# Codestacker Backend Challenge

This project is built using Django and uses SQLite Database. This django project provides the functionality of uploading PDF files to a cloud object storage, retriving files or their data, searching through the pdf files and deleting a file and all its related data.

## Running the application

1. In the project's root directory, build a docker image using the following command:`docker build --tag docker-django:latest .`
2. run the docker image: `docker run -p 8000:8000 docker-django:latest`
3. use localhost:8000 to make api calls

The APIs are protected with basic (username, password) authorization
The current superuser have the following credintials (username: nmz, password: nmz). 

#### Create a new superuser

The current superuser that is used for authentication is (username: nmz, password: nmz). If you want to create another user follow these steps:
1. Make sure you have pip and pipenv installed, if not, install them using these commands: install pip `sudo apt-get install python3-pip`, install pipenv `pip3 install pipenv`
2. Activate the virtual environment: `pipenv shell`
3. run `python manage.py createsuperuser` and follow the instructions.


## Usage

To use this project, you can make requests to the following endpoints:

### 1. UploadFile

This endpoint is used to upload a file to the server. To upload a file, make a POST request to the /upload/ endpoint with a file attached to the 'file' key in the request body .

#### URL

`pdf/upload/`

#### Method

`POST`

#### Parameters

- `file`: the file to upload.


### 2. ListFiles

This endpoint is used to list all files uploaded to the server.

#### URL

`pdf/list/`

#### Method

`GET`


### 3. Search

This endpoint is used to search for pdf files containing a keyword in addition to the sentences the keyword was in.

#### URL

`pdf/search/<str:keyword>/`

#### Method

`GET`

#### Parameters

- `keyword`: the keyword to search for in files.


### 4. FileRetrieve

This endpoint is used to retrieve a pdf file from the server.

#### URL

`pdf/get-pdf/<str:id>/`

#### Method

`GET`

#### Parameters

- `id`: the ID of the file to retrieve.

### 5. RetrieveSentences

This endpoint is used to retrieve all sentences in a file.

#### URL

`pdf/get-sentences/<str:id>/`

#### Method

`GET`

#### Parameters

- `id`: the ID of the pdf file to retrieve sentences from.


### 6. CheckOccurence

This endpoint is used to check how many times a word appears in a pdf file.

#### URL

`pdf/occurrences/<str:id>/<str:word>/`

#### Method

`GET`

#### Parameters

- `id`: the ID of the pdf file to check word occurrences in.
- `word`: the word to search for in the file.


### 7. DeleteFile

This endpoint is used to delete a pdf file and all its data.

#### URL

`pdf/delete/<str:id>/`

#### Method

`DELETE`

#### Parameters

- `id`: the ID of the file to delete.


### 8. TopWords

This endpoint is used to get the top 5 most frequent words in a pdf file.

#### URL

`pdf/top-words/<str:id>/`

#### Method

`GET`

#### Parameters

- `id`: the ID of the file to get top words from.


### 9. GetPage

This endpoint is used to retrieve a specific page in a pdf file as an image.

#### URL

`pdf/get-page/<str:id>/<int:page_number>/`

#### Method

`GET`

#### Parameters

- `id`: the ID of the file to retrieve a page from.
- `page_number`: the page number to retrieve.


