package springproject.secretsantaspring.controllers;

import lombok.AllArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import springproject.secretsantaspring.dto.CreateRoomRequest;
import springproject.secretsantaspring.model.Room;
import springproject.secretsantaspring.service.SecretSantaService;

import java.net.URI;

@RestController
@RequestMapping("/api/secret-santa")
@AllArgsConstructor
public class SecretSantaController {

    private final SecretSantaService secretSantaService;

    @GetMapping("/healthcheck")
    public String healthCheck() {
        return "OK";
    }

    @PostMapping("/room")
    public ResponseEntity<String> createRoom(@RequestBody CreateRoomRequest request) {
        Room room = secretSantaService.createRoom(request.getParticipants());
        String roomUrl = "/api/secret-santa/room/" + room.getId();
        return ResponseEntity.created(URI.create(roomUrl)).body(roomUrl);
    }

    @GetMapping("/room/{roomId}")
    public ResponseEntity<Room> getRoom(@PathVariable String roomId) {
        Room room = secretSantaService.getRoom(roomId);
        return room != null ? ResponseEntity.ok(room) : ResponseEntity.notFound().build();
    }

    @GetMapping("/room/{roomId}/participant/{participantId}")
    public ResponseEntity<String> getSecretSanta(@PathVariable String roomId, @PathVariable Long participantId) {
        String secretSanta = secretSantaService.getSecretSantaFor(roomId, participantId);
        return secretSanta != null ? ResponseEntity.ok(secretSanta) : ResponseEntity.notFound().build();
    }
}
