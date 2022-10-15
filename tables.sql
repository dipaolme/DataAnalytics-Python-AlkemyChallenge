
CREATE TABLE espacios (
    cod_localidad INTEGER,
    id_provincia INTEGER,
    id_departamento INTEGER,
    categoria TEXT,
    provincia TEXT,
    localidad TEXT,
    nombre TEXT,
    domicilio TEXT,
    codigo_postal TEXT,
    telefono TEXT,
    mail TEXT,
    web TEXT,
    fecha_carga DATE NOT NULL
);

CREATE TABLE rxcategoria (
    categoria TEXT,
    registros_totales INTEGER,
    fecha_carga DATE NOT NULL
);

CREATE TABLE rxfuente (
    fuente TEXT,
    registros_totales INTEGER,
    fecha_carga DATE NOT NULL
);

CREATE TABLE rxprovincia (
    provincia TEXT,
    categoria TEXT,
    registros_totales INTEGER,
    fecha_carga DATE NOT NULL
);

CREATE TABLE cines (
    provincia TEXT,
    pantallas INTEGER,
    butacas INTEGER,
    espacios_incaa BOOLEAN,
    fecha_carga DATE NOT NULL
);