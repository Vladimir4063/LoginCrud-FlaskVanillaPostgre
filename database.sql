CREATE TABLE task (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    task VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

SELECT * FROM task WHERE id = id

DELETE * FROM task WHERE id = id

UPDATE task SET title = %s, task, = %s, = %s WHERE id = %s