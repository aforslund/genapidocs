# genapidocs

This is a simple python script that will scan your Spring Boot REST controllers and output a simplified API specification. For when you don't want to create swagger or write documentation or install complex libraries and insert a bunch of comments into your code.  This takes instead a couple of seconds to run and will give the most basic info if it's a GET, POST, if it requires authorization, and what Java types are included. 

It assumes a team can share what the details of the return types are, often the most difficult part is just knowing where the api's are published and what the path parameters or request parameters are.

