**GraphQL: https://graphene-python.org/**

# Lecture: 1  youtube.com/playlist?list=PLOLrQ9Pn6caxz00JcLeOR-Rtq0Yi01oBH


# Installation:
pip install graphene-django


## What is GraphQL?
A query language for APIs, allowing clients to request specific data in a single request.
Flexible: Clients only fetch what they need, minimizing over-fetching and improving performance.
Powerful: Enables complex data relationships and nested queries.


## GraphQL vs. REST API:

Data Fetching	
Declarative: Clients specify exact data needs.	--> GraphQL
Imperative: Clients request specific URLs and resources. --> REST_API

Over-fetching	
Minimal: Only requested data is returned.	--> GraphQL
Common: Clients often receive unnecessary data.  --> REST_API

Data Relationships
Strong: Navigates relationships easily with nested queries.	--> GraphQL
Weak: Requires multiple requests for related data.   --> REST_API

Schema	
Explicit: Defines data structure and relationships.	 --> GraphQL
Implicit: Inferred from API endpoints and resources.  --> REST_API


## Schema in Graphene-Python:
Defines the data structure and relationships exposed by your GraphQL API.
Composed of ObjectTypes, representing models and data entities.
Fields within each object define specific data points clients can request.
Schema determines the data available and how it's accessed.

## Key Takeaways:
GraphQL offers flexibility and efficiency compared to REST APIs.
Graphene-Python simplifies schema creation and integration with Django.
Focus on defining your data structure and relationships clearly in the schema


