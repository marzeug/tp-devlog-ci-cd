package projet.microservices.employe;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.Test;

import projet.microservices.employe.application.Employe;
import projet.microservices.employe.presentation.CreationEmployeDTO;
import projet.microservices.employe.presentation.EmployeDTO;
import projet.microservices.employe.presentation.EmployeMapper;

/**
 * Tests unitaires simples du mapper (sans démarrer Spring).
 */
class EmployeMapperTest {

	EmployeMapper mapper = new EmployeMapper();

	@Test
	void testEmployeVersDTO() {
		Employe employe = new Employe(1, "Dupont");

		EmployeDTO dto = mapper.mapEmployeToEmployeDTO(employe);

		assertEquals(1, dto.getId());
		assertEquals("Dupont", dto.getNom());
	}

	@Test
	void testCreationDTOVersEmploye() {
		CreationEmployeDTO dto = new CreationEmployeDTO("Martin");

		Employe employe = mapper.mapCreationEmployeDTOToEmploye(dto);

		assertEquals("Martin", employe.getNom());
	}
}
