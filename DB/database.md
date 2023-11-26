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
