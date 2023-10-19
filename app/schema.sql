CREATE TABLE IF NOT EXISTS radcheck (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, 
    username VARCHAR(255) NOT NULL,
    attribute VARCHAR(255) NOT NULL,
    op VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS voucher (
	id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
	voucher_code VARCHAR(255) NOT NULL,
	is_active TINYINT(1) NOT NULL DEFAULT 0,
	telephone_number VARCHAR(255),
	FOREIGN KEY (voucher_code) REFERENCES radcheck(username) ON DELETE CASCADE
);

DELIMITER $$
CREATE TRIGGER voucher_insert AFTER INSERT ON radcheck
FOR EACH ROW
	BEGIN
		IF NEW.username LIKE 'omnis_%' THEN
			INSERT INTO voucher (voucher_code, is_active)
			VALUES (NEW.username, 0);
		END IF;
	END $$

DELIMITER ;

DELIMITER $$
CREATE TRIGGER voucher_update AFTER UPDATE ON radcheck
FOR EACH ROW
BEGIN
    IF OLD.username LIKE 'omnis_%' THEN
        -- Delete the old voucher entry
        DELETE FROM voucher
        WHERE voucher_code = OLD.username;
    END IF;

    IF NEW.username LIKE 'omnis_%' THEN
        -- Insert a new voucher entry with the updated username
        INSERT INTO voucher (voucher_code, is_active)
        VALUES (NEW.username, 0);
    END IF;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER voucher_delete AFTER DELETE ON radcheck
FOR EACH ROW
	BEGIN
		IF OLD.username LIKE 'omnis_%' THEN
			DELETE FROM voucher
			WHERE voucher_code = OLD.username;
		END IF;
	END $$
DELIMITER ;
