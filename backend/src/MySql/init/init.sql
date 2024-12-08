
-- Create the cards table
CREATE TABLE cards (
    username VARCHAR(50) NOT NULL,
    card_name VARCHAR(500) NOT NULL,
    PRIMARY KEY (username, card_name)
);
