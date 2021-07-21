
@RestController
@RequestMapping("/genapis")
public class GenerateAPIDocTest2 {

	@PostMapping("/generateSomething2")
	public String generateSomething2(@RequestParam int genId) {
		return "generated";
	}
}