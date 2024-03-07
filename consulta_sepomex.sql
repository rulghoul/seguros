SELECT e.nombre_estado, m.nombre_municipio, codigo_postal, CONCAT(t.nombre_tipo_asentamiento,  ' / ' , a.nombre_asentamiento ) AS nombre
FROM sepomex_asentamiento a 
JOIN sepomex_tipoasentamiento t
ON a.tipo_asentamiento_id = t.id
JOIN sepomex_municipio m
ON a.municipio_id = m.id
JOIN sepomex_estado e
ON m.estado_id = e.id
WHERE municipio_id = 6401
AND a.nombre_asentamiento LIKE 'Jardines de Morelos%';

SELECT e.nombre_estado, m.nombre_municipio, codigo_postal, CONCAT(t.nombre_tipo_asentamiento,  ' / ' , a.nombre_asentamiento ) AS nombre
FROM sepomex_asentamiento a 
JOIN sepomex_tipoasentamiento t
ON a.tipo_asentamiento_id = t.id
JOIN sepomex_municipio m
ON a.municipio_id = m.id
JOIN sepomex_estado e
ON m.estado_id = e.id
WHERE a.codigo_postal = "55070";