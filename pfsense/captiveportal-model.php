<?php

require "captiveportal-db.php";

class Model extends Db
{
    protected $table;
    private $db;
    
    public function requete(string $sql, array $attributs = null)
    {
        $this->db = Db::getInstance();
        if($attributs != null)
        {
            $query = $this->db->prepare($sql);
            try {
                $query->execute($attributs);    
            } catch (PDOException $th) {
                die($th->getMessage());
            }
            return $query;
        } else{
            try {
                return $this->db->query($sql);
            } catch (PDOException $th) {
                die($th->getMessage());
            }
        }
    }

    public function findAll()
    {
        $query = $this->requete('SELECT * FROM ' . $this->table);
        return $query->fetchAll();
    }

    public function findBy(array $criteres)
    {
        $champs = [];
        $valeurs = [];

        foreach ($criteres as $champ => $valeur) {
            $champs[] = "$champ = ?";
            $valeurs[] = $valeur;
        }

        $liste_champs = implode(' AND ', $champs);
        $result = $this->requete('SELECT * FROM ' . $this->table . ' WHERE ' . $liste_champs, $valeurs) -> fetchAll();

        if (count($result) == 1){
            return $this->requete('SELECT * FROM ' . $this->table . ' WHERE ' . $liste_champs, $valeurs) -> fetch();
        }
        return $result;
    }

    public function find(int $id)
    {
        return $this->requete('SELECT * FROM ' . $this->table . 'WHERE id = ' . $id)->fetch();
    }
}

class Radacct extends Model
{
    protected $radacctid;
    protected $acctsessionid;
    protected $username;

    public function __construct()
    {
        $this->table = "radacct";
    }
    public function getSessionID(){
        return $this->acctsessionid;
    }
    public function getUsername(){
        return $this->username;
    }
}

class Radusergroup extends Model
{
    protected $id;
    protected $username;
    protected $groupname;
    protected $priority;

    public function __construct()
    {
        $this->table = "radusergroup";   
    }
}

class Radcheck extends Model
{
    protected $id;
    protected $username;
    protected $attribute;
    protected $op;
    protected $value;

    public function __construct()
    {
        $this->table = "radcheck";
    }
}

class Radgroupcheck extends Model
{
    protected $id;
    protected $groupname;
    protected $attribute;
    protected $op;
    protected $value;

    public function __construct()
    {
        $this->table = "radgroupcheck";
    }
}