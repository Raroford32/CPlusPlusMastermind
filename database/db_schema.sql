CREATE TABLE code_samples (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    filename TEXT NOT NULL,
    content TEXT NOT NULL,
    language TEXT NOT NULL,
    file_type TEXT NOT NULL,
    categories TEXT[],
    complexity INTEGER
);

CREATE TABLE file_relationships (
    id SERIAL PRIMARY KEY,
    sample_id INTEGER REFERENCES code_samples(id),
    related_sample_id INTEGER REFERENCES code_samples(id)
);

CREATE TABLE project_structures (
    id SERIAL PRIMARY KEY,
    project_name TEXT NOT NULL,
    build_system TEXT,
    dependencies TEXT[]
);

CREATE TABLE project_files (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES project_structures(id),
    sample_id INTEGER REFERENCES code_samples(id)
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    repository_url TEXT,
    build_system TEXT,
    dependencies TEXT[]
);

CREATE INDEX idx_language ON code_samples (language);
CREATE INDEX idx_complexity ON code_samples (complexity);
CREATE INDEX idx_categories ON code_samples USING GIN (categories);
CREATE INDEX idx_file_type ON code_samples (file_type);
CREATE INDEX idx_filename ON code_samples (filename);
