<?php
require_once('captiveportal-config.php');
use PDOException;

class Db extends PDO
{
    private static $instance;

    private function __construct()
    {
        // connect au DSN
        $_dsn = 'mysql:dbname=' . DB_DATABASE . ';host=' . DB_HOST;

        // on appelle le constructeur PDO
        try {
            parent::__construct($_dsn, DB_USERNAME, DB_PASSWORD);
            $this->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            $this->setAttribute(PDO::MYSQL_ATTR_INIT_COMMAND, 'set name utf8');
            $this->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);
        } catch (PDOException $e) {
            die($e->getMessage());
        }
    }

    public static function getInstance()
    {
        if(self::$instance == null){
            self::$instance = new self();
        }
        return self::$instance;
    }
}
