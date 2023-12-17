<?php
use PDOException;

class Db extends PDO
{
    private static $instance;

    // information de connexion
    private const DBHOST = '192.168.11.251';
    private const DBUSER = 'raduser';
    private const DBPASS = 'radpass';
    private const DBNAME = 'raddb';

    private function __construct()
    {
        // connect au DSN
        $_dsn = 'mysql:dbname=' . self::DBNAME . ';host=' . self::DBHOST;

        // on appelle le constructeur PDO
        try {
            parent::__construct($_dsn, self::DBUSER, self::DBPASS);
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