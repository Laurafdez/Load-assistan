-- Enable the uuid-ossp extension if not already enabled (required for uuid generation)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create table for loads with UUID as primary key
CREATE TABLE IF NOT EXISTS loads (
    load_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
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

-- Create table for call summaries (linked by UUID)
CREATE TABLE IF NOT EXISTS call_summaries (
    id SERIAL PRIMARY KEY,
    load_id UUID NOT NULL REFERENCES loads(load_id) ON DELETE CASCADE,
    agreed_price FLOAT,
    comments TEXT,
    special_conditions VARCHAR(255),
    outcome VARCHAR, 
    sentiment VARCHAR,  
    call_duration_sec INTEGER,
    attempts INTEGER DEFAULT 1,
    counter_offers INTEGER DEFAULT 0,
    satisfaction BOOLEAN,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Sample INSERT with explicit UUIDs (only for demonstration purposes)
-- In practice, omit `load_id` to let DEFAULT uuid_generate_v4() populate it

INSERT INTO loads (
    load_id,
    origin,
    destination,
    pickup_datetime,
    delivery_datetime,
    equipment_type,
    loadboard_rate,
    notes,
    weight,
    commodity_type,
    num_of_pieces,
    miles,
    dimensions
) VALUES
-- Refrigerated
('bd051a6b-2c10-4e02-ae4e-d4e15edb56aa', 'orlando, fl', 'charlotte, nc', '2025-08-10 08:00:00', '2025-08-11 14:00:00', 'reefer', 1700, 'urgent - must arrive cold', 20000, 'dairy', 100, 590, '40x48x70'),
('c2a7e022-7fae-4e6d-b13e-38f95c26e011', 'tampa, fl', 'birmingham, al', '2025-08-10 10:00:00', '2025-08-11 18:00:00', 'reefer', 1650, 'routine delivery', 21000, 'meat', 90, 615, '40x48x70'),

-- Dry Van
('de341e22-1c4d-4b93-98f3-847ac7cb9c35', 'columbus, oh', 'nashville, tn', '2025-08-09 09:00:00', '2025-08-10 16:00:00', 'dry van', 1450, 'normal cargo', 16000, 'retail goods', 70, 430, '48x40x60'),
('f28a77ea-d72e-42c7-8ea1-9e3673f65b67', 'st. louis, mo', 'indianapolis, in', '2025-08-10 08:00:00', '2025-08-10 18:00:00', 'dry van', 1300, 'urgent - store opening', 15500, 'clothing', 60, 260, '48x40x60'),

-- Flatbed
('2f81873a-3d47-4cb5-9ef6-90c05c87fcb1', 'phoenix, az', 'el paso, tx', '2025-08-10 07:00:00', '2025-08-11 13:00:00', 'flatbed', 1800, 'oversized load', 25000, 'machinery', 30, 430, '96x48x60'),
('0f9f62ea-3af2-4d08-a1ad-774c1741340c', 'albuquerque, nm', 'oklahoma city, ok', '2025-08-11 06:00:00', '2025-08-12 15:00:00', 'flatbed', 1750, 'fragile materials', 23500, 'construction supplies', 45, 540, '96x48x72'),

-- Short distances
('39b0c3db-4713-4ec2-b325-c4f9d1ddf9f5', 'newark, nj', 'philadelphia, pa', '2025-08-12 08:00:00', '2025-08-12 14:00:00', 'dry van', 850, 'urgent delivery', 12000, 'books', 100, 95, '48x40x60'),

-- Long haul
('88d41e02-bff3-414a-b7f2-b60a4a3a4383', 'seattle, wa', 'orlando, fl', '2025-08-09 06:00:00', '2025-08-14 20:00:00', 'reefer', 3200, 'multi-stop route', 22000, 'frozen vegetables', 150, 3100, '40x48x70'),
('8f4e6f7b-f2ee-430a-a7a3-bf82b0a3ebc2', 'los angeles, ca', 'miami, fl', '2025-08-08 07:00:00', '2025-08-13 19:00:00', 'dry van', 3000, 'non-urgent', 18000, 'electronics', 80, 2750, '48x40x60'),

-- Mixed urgency
('1114a2eb-6d7e-46a0-9b98-73a46f94dd13', 'kansas city, mo', 'minneapolis, mn', '2025-08-09 10:00:00', '2025-08-10 22:00:00', 'dry van', 1400, 'delivery flexible', 17500, 'furniture', 60, 430, '48x40x60'),
('b6f43701-bdc2-4a8c-8c71-3216c7c41ab4', 'cleveland, oh', 'chicago, il', '2025-08-10 10:00:00', '2025-08-10 18:00:00', 'dry van', 1200, 'urgent - event setup', 15500, 'event materials', 55, 355, '48x40x60'),
('e01a9f2b-1af0-4e9c-9094-dde77cbdc231', 'atlanta, ga', 'jacksonville, fl', '2025-08-10 08:00:00', '2025-08-11 17:00:00', 'dry van', 1350, 'late pickup unacceptable', 17000, 'paper', 80, 350, '48x40x60'),
('fc5d97f0-d324-49d6-bf10-2b87b6b8c045', 'houston, tx', 'dallas, tx', '2025-08-09 07:00:00', '2025-08-09 15:00:00', 'dry van', 900, 'rate too low', 16000, 'auto parts', 50, 245, '48x40x60'),
('4f3bc189-f69e-4b1c-a2aa-5f5c308a71e0', 'salt lake city, ut', 'boise, id', '2025-08-08 06:00:00', '2025-08-09 18:00:00', 'reefer', 1500, 'cold chain required', 21000, 'vegetables', 90, 350, '40x48x70'),
('5a912d9d-2c59-4cc7-bec6-d1995bafc410', 'denver, co', 'wichita, ks', '2025-08-10 10:00:00', '2025-08-11 20:00:00', 'flatbed', 1600, 'requires follow-up call', 24000, 'metal sheets', 40, 500, '96x48x72');



-- Call summaries referencing UUIDs above
INSERT INTO call_summaries (
    load_id,
    agreed_price,
    comments,
    special_conditions,
    outcome,
    sentiment,
    call_duration_sec,
    attempts,
    counter_offers,
    satisfaction
) VALUES
(
    'bd051a6b-2c10-4e02-ae4e-d4e15edb56aa',
    1450.00,
    'Accepted with minor delay flexibility',
    'None',
    'accepted',
    'positive',
    315,
    1,
    0,
    TRUE
),
(
    'c2a7e022-7fae-4e6d-b13e-38f95c26e011',
    1750.00,
    'Carrier confirmed urgency, agreed to unload early',
    'Priority unloading',
    'accepted',
    'positive',
    420,
    1,
    1,
    TRUE
),
(
    'de341e22-1c4d-4b93-98f3-847ac7cb9c35',
    1600.00,
    'Carrier wants follow-up next week',
    'Wants morning pickup',
    'interested_follow_up',
    'positive',
    280,
    1,
    0,
    TRUE
),
(
    'e01a9f2b-1af0-4e9c-9094-dde77cbdc231',
    NULL,
    'Carrier declined due to tight schedule',
    'Strict delivery window',
    'rejected',
    'negative',
    180,
    2,
    1,
    FALSE
),
(
    'fc5d97f0-d324-49d6-bf10-2b87b6b8c045',
    NULL,
    'Price negotiation failed, rate too low',
    NULL,
    'failed_negotiation',
    'neutral',
    240,
    3,
    2,
    FALSE
),
(
    '4f3bc189-f69e-4b1c-a2aa-5f5c308a71e0',
    NULL,
    'No answer after multiple attempts',
    NULL,
    'no_response',
    'neutral',
    NULL,
    4,
    0,
    NULL
),
(
    '5a912d9d-2c59-4cc7-bec6-d1995bafc410',
    NULL,
    'Carrier asked to be contacted tomorrow',
    'Prefers late morning call',
    'interested_follow_up',
    'positive',
    210,
    2,
    0,
    TRUE
);
