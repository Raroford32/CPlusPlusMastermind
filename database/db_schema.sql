CREATE TABLE code_samples (
    id SERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    filename TEXT NOT NULL,
    content TEXT NOT NULL,
    language TEXT NOT NULL,
    categories TEXT[],
    complexity INTEGER
);

CREATE INDEX idx_language ON code_samples (language);
CREATE INDEX idx_complexity ON code_samples (complexity);
CREATE INDEX idx_categories ON code_samples USING GIN (categories);
