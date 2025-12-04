package springproject.secretsantaspring.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import springproject.secretsantaspring.model.Participant;

public interface ParticipantRepository extends JpaRepository<Participant, Long> {
}
