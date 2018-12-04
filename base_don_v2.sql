-- Creation of the database --
CREATE TABLE IF NOT EXISTS drinks (id INTEGER PRIMARY KEY, name VARCHAR(30), container_size INTEGER, threshold INTEGER, by_bottle BOOLEAN DEFAULT 0,is_champagne BOOLEAN DEFAULT 0);
CREATE TABLE IF NOT EXISTS food (id INTEGER PRIMARY KEY, name VARCHAR(30))
CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, name VARCHAR(30), ip VARCHAR(15), connected BOOLEAN DEFAULT 1);
CREATE TABLE IF NOT EXISTS stocks (id INTEGER PRIMARY KEY, room INTEGER, drink INTEGER, quantity INTEGER, FOREIGN KEY(drink) REFERENCES drinks(id), FOREIGN KEY(room) REFERENCES rooms(id));
CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, drink INTEGER, room INTEGER, stamp DATETIME, quantity INTEGER DEFAULT 1, is_sale BOOLEAN DEFAULT 1, is_cancelled BOOLEAN DEFAULT 0, FOREIGN KEY(drink) REFERENCES drinks(id), FOREIGN KEY(room) REFERENCES rooms(id));
-- Filling the tables --
-- Creating drinks --
  -- By drink - 6 / box --
INSERT INTO drinks(name, container_size, threshold, by_bottle, is_champagne) VALUES('Cordeliers', 42, 42, 1, 1);
INSERT INTO drinks(name, container_size, threshold, by_bottle, is_champagne) VALUES('Cordeliers Rosé', 42, 42, 1, 1);
INSERT INTO drinks(name, container_size, threshold, by_bottle, is_champagne) VALUES('Cordeliers Vintage', 42, 42, 1, 1);
  -- Can sell Magnum = double bottle --
INSERT INTO drinks(name, container_size, threshold, by_bottle) VALUES('Jacquart Brut', 42, 84, 1);
  -- By bottle - 6 / box --
INSERT INTO drinks(name, container_size, threshold) VALUES('Jacquart Rosé', 6, 6);
  -- By bottle - bottle / bottle - on demand --
INSERT INTO drinks(name, container_size, threshold) VALUES('Moët & Chandon', 1, 0);
INSERT INTO drinks(name, container_size, threshold) VALUES('Deutz Brut', 1, 0);
INSERT INTO drinks(name, container_size, threshold) VALUES('Veuve Clicquot', 1, 0);
INSERT INTO drinks(name, container_size, threshold) VALUES('Ruinart Brut', 1, 0);
INSERT INTO drinks(name, container_size, threshold) VALUES('Dom Perignon', 1, 0);
  -- Cocktail by drink --
INSERT INTO drinks(name, container_size, threshold) VALUES('Etincelle', 17, 17);
INSERT INTO drinks(name, container_size, threshold) VALUES('Euréka', 16, 16);
INSERT INTO drinks(name, container_size, threshold) VALUES('Atome', 12, 12);
INSERT INTO drinks(name, container_size, threshold) VALUES('Eclair', 20, 20);
-- Creating food --
INSERT INTO food(name) VALUES ('Tapas');
-- Creating rooms --
INSERT INTO rooms(name, ip, connected) VALUES('reserve', '', 0);
INSERT INTO rooms(name, ip, connected) VALUES('tesla', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('edison', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('eiffel', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('vinci', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('kve', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('cdf', '', 0)
INSERT INTO rooms(name, ip, connected) VALUES('restal', '', 0)
-- Filling initial stocks --
-- Tesla --
INSERT INTO stocks(room, drink, quantity) VALUES(1, 1, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 3, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 4, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 6, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 11, 51);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 13, 36);
INSERT INTO stocks(room, drink, quantity) VALUES(1, 14, 60);
-- Edison --
INSERT INTO stocks(room, drink, quantity) VALUES(2, 1, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 4, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 9, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 11, 51);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 13, 36);
INSERT INTO stocks(room, drink, quantity) VALUES(2, 14, 60);
-- Eiffel --
INSERT INTO stocks(room, drink, quantity) VALUES(3, 1, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 3, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 4, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 6, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 9, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 11, 51);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 12, 48);
INSERT INTO stocks(room, drink, quantity) VALUES(3, 14, 60);
-- Vinci --
INSERT INTO stocks(room, drink, quantity) VALUES(4, 1, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 4, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 12, 48);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 13, 36);
INSERT INTO stocks(room, drink, quantity) VALUES(4, 14, 60);
-- K'Ve --
INSERT INTO stocks(room, drink, quantity) VALUES(5, 1, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 2, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 3, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 4, 168);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 5, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 6, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 7, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 8, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 9, 6);
INSERT INTO stocks(room, drink, quantity) VALUES(5, 10, 0);