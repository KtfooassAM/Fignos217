-- Creation of the database --
CREATE TABLE IF NOT EXISTS drinks (id INTEGER PRIMARY KEY, name VARCHAR(30), container_size INTEGER, threshold INTEGER, by_bottle BOOLEAN DEFAULT 0,is_champagne BOOLEAN DEFAULT 0);
CREATE TABLE IF NOT EXISTS food (id INTEGER PRIMARY KEY, name VARCHAR(30))
CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, name VARCHAR(30), ip VARCHAR(15), connected BOOLEAN DEFAULT 1, is_bar BOOLEAN DEFAULT 0);
CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY, room INTEGER, drink INTEGER, quantity INTEGER, consommation INTEGER DEFAULT 0, FOREIGN KEY(drink) REFERENCES drinks(id), FOREIGN KEY(room) REFERENCES rooms(id));
CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, drink INTEGER, room INTEGER, stamp DATETIME, quantity INTEGER DEFAULT 1, is_sale BOOLEAN DEFAULT 1, is_cancelled BOOLEAN DEFAULT 0, FOREIGN KEY(drink) REFERENCES drinks(id), FOREIGN KEY(room) REFERENCES rooms(id));
-- Filling the tables --
-- Creating drinks --
  -- By drink - 6 / box --
INSERT INTO drinks(name, container_size, threshold, by_bottle, is_champagne) VALUES('Prosecco', 42, 42, 1, 1);
INSERT INTO drinks(name, container_size, threshold, by_bottle, is_champagne) VALUES('Jacquart Brut', 42, 42, 1, 1);
  -- Can sell Magnum = double bottle --
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Jacquart Magnum', 42, 84, 1);
  -- By bottle - 6 / box --
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Prosecco', 6, 6, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Jacquart Rosé', 6, 6, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Jacquart Brut', 6, 6, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Moët&Chandon', 6, 6, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Ruinard', 6, 6, 1);
  -- By bottle - bottle / bottle - on demand --
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Prosecco', 1, 0, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Jacquart Rosé', 1, 0, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Jacquart Brut', 1, 0, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Moët&Chandon', 1, 0, 1);
INSERT INTO drinks(name, container_size, threshold, is_champagne) VALUES('Ruinard', 1, 0, 1);
  -- Cocktail by drink --
INSERT INTO drinks(name, container_size, threshold) VALUES('Gondola azurra', 17, 17);
INSERT INTO drinks(name, container_size, threshold) VALUES('Mexico', 17, 17);
INSERT INTO drinks(name, container_size, threshold) VALUES('Lamdaba', 17, 17);
INSERT INTO drinks(name, container_size, threshold) VALUES('Ming', 17, 17);
-- Creating food --
INSERT INTO food(name) VALUES ('Tapas');
-- Creating rooms --
INSERT INTO rooms(name, ip, connected, is_bar) VALUES('chine', '', 0, 1)
INSERT INTO rooms(name, ip, connected, is_bar) VALUES('venise', '', 0, 1)
INSERT INTO rooms(name, ip, connected, is_bar) VALUES('rio', '', 0, 1)
INSERT INTO rooms(name, ip, connected, is_bar) VALUES('mexico', '', 0, 1)
INSERT INTO rooms(name, ip, connected, is_bar) VALUES('kve', '', 0, 1)
INSERT INTO rooms(name, ip, connected) VALUES('reserve', '', 0);
INSERT INTO rooms(name, ip, connected) VALUES('cdf', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('restal', '', 0)
-- Filling initial stocks --
-- Chine --
INSERT INTO stocks(room, drink, quantity) VALUES(1, 1, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 3, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 6, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 17, 17);
-- Venise --
INSERT INTO stocks(room, drink, quantity) VALUES(2, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 3, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 4, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 14, 17);
-- Rio --
INSERT INTO stocks(room, drink, quantity) VALUES(3, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 3, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 4, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 16, 17);
-- Mexico --
INSERT INTO stocks(room, drink, quantity) VALUES(4, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 3, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 4, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 14, 17);
-- K'Ve -
INSERT INTO stocks(room, drink, quantity) VALUES(5, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 3, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 4, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 17, 17);