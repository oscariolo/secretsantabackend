package springproject.secretsantaspring.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import springproject.secretsantaspring.model.Room;

public interface RoomRepository extends JpaRepository<Room, String> {
}
