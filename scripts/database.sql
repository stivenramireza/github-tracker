-- Create the extension for uuid support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create the commits table
CREATE TABLE commits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  repo_name VARCHAR(255) NOT NULL,
  commit_id VARCHAR(255) NOT NULL,
  commit_message TEXT,
  author_username VARCHAR(255) NOT NULL,
  author_email VARCHAR(255) NOT NULL,
  payload TEXT,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
