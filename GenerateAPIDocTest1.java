
@RestController
public class GenerateAPIDocTest1 {

	@GetMapping("/generateSomething/{genId}")
	public String generateSomething(@PathVariable int genId) {
		return "generated";
	}
}