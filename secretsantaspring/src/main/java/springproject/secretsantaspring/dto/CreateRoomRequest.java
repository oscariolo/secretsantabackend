package springproject.secretsantaspring.dto;

import lombok.Data;

import java.util.List;

@Data
public class CreateRoomRequest {
    private List<String> participants;
}
