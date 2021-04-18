## Get course by id
curl "http://localhost:5000/course/101"

## Get default page of courses
curl "http://localhost:5000/course"

## Get nth page of courses
curl "http://localhost:5000/course?page-number=20&page-size=10"

## Get page of courses by title words
curl "http://localhost:5000/course?title-words=django,%20python"

## Delete course by id
curl -X "DELETE" "http://localhost:5000/course/201"

## Add course
curl -X "POST" "http://localhost:5000/course" \
     -H 'Content-Type: application/json' \
     -d $'{
  "description": "This is a brand new course",
  "discount_price": 5,
  "title": "Brand new course",
  "price": 25,
  "image_path": "images/some/path/foo.jpg",
  "on_discount": false
}'

## Add course with errors
curl -X "POST" "http://localhost:5000/course" \
     -H 'Content-Type: application/json' \
     -d $'{
  "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
  "discount_price": 5,
  "title": "X",
  "price": 12,
  "image_path": "images/some/path/foo.jpg",
  "on_discount": false
}'

## Update course
curl -X "PUT" "http://localhost:5000/course/201" \
     -H 'Content-Type: application/json' \
     -d $'{
  "image_path": "images/some/path/foo.jpg",
  "discount_price": 5,
  "id": 201,
  "price": 25,
  "title": "Blah blah blah",
  "on_discount": false,
  "description": "New description"
}'

## Update course with errors
curl -X "PUT" "http://localhost:5000/course/201" \
     -H 'Content-Type: application/json' \
     -d $'{
  "image_path": "images/some/path/foo.jpg",
  "discount_price": 5,
  "id": "OOO",
  "price": 25,
  "title": "X",
  "on_discount": "X",
  "description": "New description"
}'
