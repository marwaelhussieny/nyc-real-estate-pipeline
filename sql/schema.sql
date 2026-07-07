-- Target table shape after load.py runs. Created implicitly via pandas.to_sql,
-- documented here for reference / for anyone reproducing this by hand.

CREATE TABLE IF NOT EXISTS nyc_property_sales (
    borough                     INTEGER,
    neighborhood                TEXT,
    building_class_category     TEXT,
    tax_class_at_present         TEXT,
    block                       BIGINT,
    lot                         BIGINT,
    ease_ment                   TEXT,
    building_class_at_present    TEXT,
    address                     TEXT,
    apartment_number             TEXT,
    zip_code                    INTEGER,
    residential_units            INTEGER,
    commercial_units             INTEGER,
    total_units                 INTEGER,
    land_square_feet             DOUBLE PRECISION,
    gross_square_feet            DOUBLE PRECISION,
    year_built                  INTEGER,
    tax_class_at_time_of_sale      INTEGER,
    building_class_at_time_of_sale  TEXT,
    sale_price                  DOUBLE PRECISION,
    sale_date                   TIMESTAMP,
    borough_name                TEXT,
    is_arms_length_sale          BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_sales_borough ON nyc_property_sales (borough);
CREATE INDEX IF NOT EXISTS idx_sales_date ON nyc_property_sales (sale_date);
CREATE INDEX IF NOT EXISTS idx_sales_zip ON nyc_property_sales (zip_code);
