CREATE TABLE IF NOT EXISTS loads (
    load_id VARCHAR PRIMARY KEY,
    origin VARCHAR,
    destination VARCHAR,
    pickup_datetime TIMESTAMP,
    delivery_datetime TIMESTAMP,
    equipment_type VARCHAR,
    loadboard_rate FLOAT,
    notes TEXT,
    weight FLOAT,
    commodity_type VARCHAR,
    num_of_pieces INT,
    miles FLOAT,
    dimensions VARCHAR
);

CREATE TABLE IF NOT EXISTS call_summaries (
    id SERIAL PRIMARY KEY,
    load_id VARCHAR REFERENCES loads(load_id),
    agreed_price FLOAT,
    comments TEXT,
    special_conditions VARCHAR(255),
    outcome VARCHAR,
    sentiment VARCHAR
);


INSERT INTO loads VALUES (
    'L001', 'Miami, FL', 'Atlanta, GA', '2025-07-30 08:00:00', '2025-07-31 17:00:00',
    'Dry Van', 1500.0, 'Fragile cargo', 20000, 'Electronics', 100, 660, '48x40x60'
);
