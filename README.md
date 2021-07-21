# Generate API documentation for Spring Boot RestControllers

This is a simple python script that will scan your Spring Boot REST controllers and output a simplified API specification. For when you don't want to create swagger or write documentation or install complex libraries and insert a bunch of comments into your code.  This takes instead a couple of seconds to run and will give the most basic info if it's a GET, POST, if it requires authorization, and what Java types are included. 

It assumes a team can share what the details of the return types are, often the most difficult part is just knowing where the api's are published and what the path parameters or request parameters are.

Why is it written in Python?  Because it's fun, but also simple to execute on the command-line.

It is executed as follows:

```
python3 GenerateAPIDocsForSpringBoot.py <directory> <outputFile>
```

## Example

Given the following two Spring java files:

```
@RestController
public class GenerateAPIDocTest1 {

        @GetMapping("/generateSomething/{genId}")
        public String generateSomething(@PathVariable int genId) {
                return "generated";
        }
```
```
@RestController
@RequestMapping("/genapis")
public class GenerateAPIDocTest2 {

	@PostMapping("/generateSomething2")
	public String generateSomething2(@RequestParam int genId) {
		return "generated";
	}
}
```

Then the output when running the script will be:

```
** Generating API Docs **

* Reading files from '.'
* Outputting to 'apioutput.txt'

* Processing: GenerateAPIDocTest2.java
* Processing: GenerateAPIDocTest1.java

Processing complete.  Total 2 APIs found
```

And the API definition file will contain:

```
HTTP POST /genapis/generateSomething2
    Parameters: @RequestParam int genId
    Returns: String

HTTP GET /generateSomething/{genId}
    Parameters: @PathVariable int genId
    Returns: String
```

## Enhancements

To be more complete, in particular all HTTP methods should be supported, and probably there are lots of other missing annotations and formatting that would be good to add. Anyone is welcome to contribute to make it more complete, and there's probably a lot that could be done to improve the python code itself.

