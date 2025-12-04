package springproject.secretsantaspring.service;

import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import springproject.secretsantaspring.model.Participant;
import springproject.secretsantaspring.model.Room;
import springproject.secretsantaspring.repository.RoomRepository;

import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Service
@AllArgsConstructor
public class SecretSantaService {

    private final RoomRepository roomRepository;

    public Room createRoom(List<String> participantNames) {
        Room room = new Room();
        List<Participant> participants = participantNames.stream()
                .map(name -> {
                    Participant p = new Participant();
                    p.setName(name);
                    p.setRoom(room);
                    return p;
                })
                .collect(Collectors.toList());
        room.setParticipants(participants);
        assignSecretSantas(participants);
        return roomRepository.save(room);
    }

    private void assignSecretSantas(List<Participant> participants) {
        Collections.shuffle(participants);
        for (int i = 0; i < participants.size(); i++) {
            participants.get(i).setSecretSantaFor(participants.get((i + 1) % participants.size()));
        }
    }

    public Room getRoom(String roomId) {
        return roomRepository.findById(roomId).orElse(null);
    }

    public String getSecretSantaFor(String roomId, Long participantId) {
        Room room = getRoom(roomId);
        if (room != null) {
            for (Participant p : room.getParticipants()) {
                if (p.getId().equals(participantId)) {
                    return p.getSecretSantaFor().getName();
                }
            }
        }
        return null;
    }
}
