-- PostgreSQL extensions for the doctor management database
-- This script runs once when the Docker PostgreSQL container initializes.

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- for fuzzy text search
