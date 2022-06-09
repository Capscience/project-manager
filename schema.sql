CREATE TABLE account (
        id SERIAL NOT NULL, 
        name VARCHAR(32), 
        password VARCHAR(128), 
        PRIMARY KEY (id)
)

CREATE TABLE work_type (
        id SERIAL NOT NULL, 
        name VARCHAR(32), 
        rounding NUMERIC, 
        minimum NUMERIC, 
        price NUMERIC, 
        PRIMARY KEY (id), 
        UNIQUE (name)
)

CREATE TABLE company (
        id SERIAL NOT NULL, 
        name VARCHAR(32), 
        user_id INTEGER, 
        PRIMARY KEY (id), 
        UNIQUE (name), 
        FOREIGN KEY(user_id) REFERENCES account (id) ON DELETE CASCADE
)

CREATE TABLE project (
        id SERIAL NOT NULL, 
        state INTEGER, 
        name VARCHAR(128), 
        user_id INTEGER, 
        company_id INTEGER, 
        type_id INTEGER, 
        PRIMARY KEY (id), 
        FOREIGN KEY(user_id) REFERENCES account (id) ON DELETE CASCADE, 
        FOREIGN KEY(company_id) REFERENCES company (id) ON DELETE CASCADE, 
        FOREIGN KEY(type_id) REFERENCES work_type (id)
)

CREATE TABLE entry (
        id SERIAL NOT NULL, 
        project_id INTEGER, 
        starttime TIMESTAMP WITHOUT TIME ZONE, 
        endtime TIMESTAMP WITHOUT TIME ZONE, 
        comment VARCHAR(128), 
        PRIMARY KEY (id), 
        FOREIGN KEY(project_id) REFERENCES project (id) ON DELETE CASCADE
)