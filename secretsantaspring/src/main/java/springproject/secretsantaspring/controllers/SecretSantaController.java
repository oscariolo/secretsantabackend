package springproject.secretsantaspring.controllers;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/secret-santa")
public class SecretSantaController {

    @GetMapping("/healthcheck")
    public String healthCheck() {
        return "OK";
    }
    
}
