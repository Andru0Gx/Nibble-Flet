# Nibble DataBase (DB)

> Breve descripcion de la base de datos del sistema Nibble.

## Tablas
```md

1. Estudiantes
2. Profesores
3. Materias
4. Notas
5. Horarios
6. Usuario
7. Calendario

```

> Las tablas de usuarios, profesores, estudiantes y materias son las tablas principales, las cuales se relacionan con las demas tablas.

> Las tablas Usuario, Calendario y Configuraciones no se relacionan con ninguna otra tabla.

**Tabla Usuario**
```md

1. ID
2. Usuario
3. Correo
4. Contraseña
5. Respuesta De Seguridad 1
6. Respuesta De Seguridad 2
7. Respuesta De Seguridad 3

```

> Solo se puede registrar un Usuario.

**Tabla Calendario**
```md

1. ID Evento
2. Nombre Evento
3. Descripcion Evento
4. Fecha Evento

```

**Tabla Estudiantes**
```md

1. Cedula Estudiante
2. Nombre Estudiante
3. Apellido Estudiante
4. Fecha Nacimiento Estudiante
6. Telefono1 Estudiante
7. Telefono2 Estudiante
8. Direccion Estudiante
9. Correo Estudiante
10. Etapa_id Estudiante

```

**Tabla Profesores**
```md

1.  Cedula Profesor
2.  Nombre Profesor
3.  Apellido Profesor
4.  Fecha Nacimiento Profesor
5.  Telefono1 Profesor
6.  Telefono2 Profesor
7.  Direccion Profesor
8.  Correo Profesor

```

**Tabla Materias**
```md

1. ID Materia
2. Nombre Materia

```

**Tabla Notas**
```md

1. ID Nota
2. Estudiante_id Nota
3. Materia_id Nota
4. Momento Nota
5. Nro_Actividad Nota
6. Descripcion_Actividad Nota
7. Calificacion Nota
8. Fecha Nota

```

**Tabla Horarios**

> Posibles Campos

```md

1. ID Horario
2. Profesor_id Horario
3. Materia_id Horario
4. Dia Horario
5. Hora_Inicio Horario

```
