document.getElementById("formulario").addEventListener("submit", async function (event) {
  event.preventDefault();  // Evita el comportamiento por defecto del formulario

  // Recoger los datos del formulario
  const formData = {
    frecuencia_musica: document.getElementById("frecuencia_musica").value,
    franja_horaria: document.getElementById("franja_horaria").value,
    estado_animo: document.getElementById("estado_animo").value,
    genero: document.getElementById("genero").value,
    edad: document.getElementById("edad").value,
    genero_musical: document.getElementById("genero_musical").value,
  };

  try {
    // Enviar los datos a la API usando fetch
    const response = await fetch("http://localhost:8000/recomendar", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",  // Aseguramos que se envíen como JSON
      },
      body: JSON.stringify(formData),  // Convertimos los datos del formulario a JSON
    });

    if (!response.ok) {
      throw new Error("Error en la solicitud");
    }

    // Obtener las recomendaciones
    const data = await response.json();

    // Mostrar las recomendaciones
    const recomendacionesLista = document.getElementById("recomendaciones-lista");
    recomendacionesLista.innerHTML = '';  // Limpiar cualquier recomendación previa

    data.recomendaciones.forEach(recomendacion => {
      const li = document.createElement("li");
      li.textContent = `${recomendacion.song_name} - ${recomendacion.artist_name}`;
      recomendacionesLista.appendChild(li);
    });
  } catch (error) {
    console.error("Error:", error);
  }
});
