-- schema.sql

-- Users Table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Wastes Table
CREATE TABLE wastes (
    id SERIAL PRIMARY KEY,
    material_type VARCHAR NOT NULL,
    description TEXT,
    weight_kg FLOAT,
    image_url VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    uploader_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Products Table
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description TEXT,
    image_url VARCHAR NOT NULL,
    price_points INTEGER NOT NULL,
    status VARCHAR NOT NULL,
    upcycler_id INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Transactions Table
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL REFERENCES products(id),
    buyer_id INTEGER NOT NULL REFERENCES users(id),
    seller_id INTEGER NOT NULL REFERENCES users(id),
    points_exchanged INTEGER NOT NULL,
    transaction_time TIMESTAMPTZ DEFAULT NOW()
);

-- Points Ledger Table
CREATE TABLE points_ledger (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    points_change INTEGER NOT NULL,
    reason VARCHAR NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);