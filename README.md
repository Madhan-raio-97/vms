# Vendor Management System with Performance Metrics

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Madhan-raio-97/vms.git
$ cd vms
```

Create a virtual environment to install dependencies in and activate it: For Ubuntu or Mac.

```sh
$ python3 -m venv venv
$ source venv/bin/activate
```

Create a virtual environment to install dependencies in and activate it: For Windows.

```sh
$ python -m venv venv
$ cd venv/scripts/
$ activate
```

Then install the dependencies:

```sh
(venv)$ cd vms
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Once `pip` has finished downloading the dependencies:

Start migrations:

```sh
(venv)$ cd vms
(venv)$ python manage.py makemigrations vendor
(venv)$ python manage.py makemigrations purchaseorder
(venv)$ python manage.py migrate
```
Create SuperUser For Authentication purpose:

```sh
(venv)$ cd vms
(venv)$ python manage.py createsuperuser
```
Now Run Project:

```sh
(venv)$ cd vms
(venv)$ python manage.py runserver
```

Now Check the browser: http://localhost:8000/auth/login/

## Setup optional sample data load

if we need to dump dummy data for VENDOR use this command:

```sh
(venv)$ cd vms
(venv)$ python manage.py loaddata vendor.json
```


## Test Case done for developed API Endpoint by using Django Rest Framework:

using this command to test the endpoint working as expected.

```sh
(venv)$ cd vms
(venv)$ python manage.py test
```


Documentation for each of the API endpoints:

1. **Vendor List and Create Endpoint**
   - URL: `/api/vendors/`
   - HTTP Method: GET (for retrieving list), POST (for creating new vendor)
   - Description: This endpoint allows you to retrieve a list of vendors or create a new vendor.
   - Parameters:
     - None required for GET request.
     - For POST request, include a JSON object representing the new vendor.
        ```sh
        {
            "name": "DBC Solutions",
            "contact_details": "info@dbcsolutions.com",
            "address": "345 Pine Lane, Hilltop, USA",
            "vendor_code": "VENDOR020"
        }
        ```
   - Response:
     - GET: Returns a list of existing vendors in JSON format.
        ```sh
        [
            {
                "id": 1,
                "name": "ABC Electronics",
                "contact_details": "contact@abcelectronics.com",
                "address": "123 Main Street, Cityville, USA",
                "vendor_code": "VENDOR001",
                "on_time_delivery_rate": 0.0,
                "quality_rating_avg": 0.0,
                "average_response_time": 0.0,
                "fulfillment_rate": 0.0
            },
            {
                "id": 2,
                "name": "XYZ Supplies",
                "contact_details": "info@xyzsupplies.com",
                "address": "456 Oak Avenue, Townsville, USA",
                "vendor_code": "VENDOR002",
                "on_time_delivery_rate": 0.0,
                "quality_rating_avg": 0.0,
                "average_response_time": 0.0,
                "fulfillment_rate": 0.0
            }
        ]
        ```
     - POST: Returns the newly created vendor in JSON format with status code 201 (Created).
        ```sh
        {
            "id": 21,
            "name": "DBC Solutions",
            "contact_details": "info@dbcsolutions.com",
            "address": "345 Pine Lane, Hilltop, USA",
            "vendor_code": "VENDOR021"
        }
        ```

2. **Vendor Detail Endpoint**
   - URL: `/api/vendors/<int:vendor_id>/`
   - HTTP Method: GET (for retrieving vendor details), PUT (for updating vendor details), DELETE (for deleting vendor)
   - Description: This endpoint allows you to retrieve, update, or delete a specific vendor identified by `vendor_id`.
   - Parameters:
     - `vendor_id`: ID of the vendor (integer) in the URL path.
   - Response:
     - GET: Returns the details of the specified vendor in JSON format.
     - PUT: Updates the details of the specified vendor and returns the updated vendor in JSON format.
     - DELETE: Deletes the specified vendor and returns status code 204 (No Content).

3. **Purchase Order List and Create Endpoint**
   - URL: `/api/purchase_orders/`
   - HTTP Method: GET (for retrieving list), POST (for creating new purchase order)
   - Description: This endpoint allows you to retrieve a list of purchase orders or create a new purchase order.
   - Parameters:
     - None required for GET request.
     - For POST request, include a JSON object representing the new purchase order.
   - Response:
     - GET: Returns a list of existing purchase orders in JSON format.
     - POST: Returns the newly created purchase order in JSON format with status code 201 (Created).

4. **Purchase Order Detail Endpoint**
   - URL: `/api/purchase_orders/<int:pk>/`
   - HTTP Method: GET (for retrieving purchase order details), PUT (for updating purchase order details), DELETE (for deleting purchase order)
   - Description: This endpoint allows you to retrieve, update, or delete a specific purchase order identified by `pk`.
   - Parameters:
     - `pk`: Primary key of the purchase order (integer) in the URL path.
   - Response:
     - GET: Returns the details of the specified purchase order in JSON format.
     - PUT: Updates the details of the specified purchase order and returns the updated purchase order in JSON format.
     - DELETE: Deletes the specified purchase order and returns status code 204 (No Content).

5. **Vendor Performance Endpoint**
   - URL: `/api/vendors/<int:vendor_id>/performance/`
   - HTTP Method: GET
   - Description: This endpoint allows you to retrieve the performance metrics of a specific vendor identified by `vendor_id`.
   - Parameters:
     - `vendor_id`: ID of the vendor (integer) in the URL path.
   - Response: Returns the performance metrics of the specified vendor in JSON format.

6. **Acknowledge Purchase Order Endpoint**
   - URL: `/api/purchase_orders/<int:po_id>/acknowledge/`
   - HTTP Method: POST
   - Description: This endpoint allows you to acknowledge a specific purchase order identified by `po_id`.
   - Parameters:
     - `po_id`: ID of the purchase order (integer) in the URL path.
   - Response: Returns status code 200 (OK) upon successful acknowledgment of the purchase order.

These endpoints provide a comprehensive set of functionalities for managing vendors, purchase orders, and their related operations.
