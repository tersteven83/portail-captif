<!--<?php
    require "captiveportal-model.php";
    $radacct = new Radacct;
    $radgroupcheck = new Radgroupcheck;
    $radusergroup = new Radusergroup;
    $radcheck = new Radcheck;

    // trouver l'utilisateur portant le numéro se session
    $session = $radacct->findBy(['acctsessionid' => $sessionid]);
    $username = $session->username;

    // recupérer le profil de l'utilisateur

    $profils = $radusergroup->findBy(['username' => $username]);
    $user_profils = [];
    foreach ($profils as $profil) {
        // verifier si le profil n'est pas déjà dans le tableau de profil de l'utilisateur
        if (!in_array($profil->groupname, $user_profils)) {
            $user_profils[] = $profil->groupname;
        }
    }


    //checké si l'utilisateur a un attribute login-time qq part
    $userCheckAttr = $radcheck->findBy(['username' => $username]);
    $plage_entry = null;
    $expiration = null;
    foreach ($userCheckAttr as $checkAttr) {
        if ($checkAttr->attribute == "Login-Time") {
            $plage_entry = $checkAttr->value;
            break;
        }
        if ($checkAttr->attribute == "Expiration") {
            $expiration = $checkAttr->value;
            break;
        }
    }
    if ($plage_entry == null) {
        // vérifier si il y a un attribut login-time parmi les attributs du profil
        foreach ($user_profils as $user_profil) {
            $gpAttrCheks = $radgroupcheck->findBy(['groupname' => $user_profil]);
            foreach ($gpAttrCheks as $gpAttrChek) {
                if ($gpAttrChek->attribute == "Login-Time") {
                    $plage_entry = $gpAttrChek->value;
                    break;
                }
            }
        }
        if ($plage_entry == null) $plage_entry = "Toute heure";
    }
    if ($expiration == null) {
        foreach ($user_profils as $user_profil) {
            $gpAttrCheks = $radgroupcheck->findBy(['groupname' => $user_profil]);
            foreach ($gpAttrCheks as $gpAttrChek) {
                if ($gpAttrChek->attribute == "Expiration") {
                    $expiration = $gpAttrChek->value;
                    break;
                }
            }
        }
        if ($expiration == null) $expiration = '-';
    }
    // echo $sessionid;

    ?>
-->




<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- Bootstrap CSS CDN -->

    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" integrity="sha512-nNEKUmEaX6jxKjz0LHF1t53QBNErEYHU2Ya4xhdX5n4cNAqkIbwBtWJtsMlFm3qg6MeO6lGGxPmSX6b5bIVvKw==" crossorigin="anonymous" referrerpolicy="no-referrer" />

    <!-- Font Awesome JS -->
    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/solid.js" integrity="sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ" crossorigin="anonymous"></script>
    <script defer src="https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js" integrity="sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY" crossorigin="anonymous"></script>


    <!-- jQuery CDN - Slim version (=without AJAX) -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <!-- Popper.JS -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" crossorigin="anonymous"></script>
    <!-- Bootstrap JS -->
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" crossorigin="anonymous"></script>
    <link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css'>

    <style>
        body {
            margin: 0;
            padding: 0;
            background-image: url('captiveportal-bg-logout.jpg'); /* Replace 'your-image-url.jpg' with the path to your image */
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            height: 100vh; /* Set the height of the background to 100% of the viewport height */
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>

    <title>Invité</title>
</head>

<body>
    <div class="container-fluid">
        <section class="gradient-custom">
            <div class="container py-5">
                <div class="row justify-content-center align-items-center">
                    <div class="col-12 col-lg-9 col-xl-7">
                        <div class="card shadow-2-strong card-registration" style="border-radius: 15px;">
                            <div class="card-body p-4 p-md-5" style="background-color: rgba(4, 29, 33, 0.334);background-repeat:no-repeat; background-position:center;background-size: cover; padding: 20px;box-sizing: border-box;opacity: 5;border-radius: 8px;">
                                <h3 class="mb-4 pb-2 pb-md-0 mb-md-5" style="background-color: rgba(241, 235, 235, 0.388); font-family: cursive; font-weight: bolder;">Vous êtes connecté à l'internet</h3>
                                <form action="<?= $logouturl ?>" method="post">
                                    <input name="logout_id" type="hidden" value="<?= $sessionid; ?>">
                                    <input name="zone" type="hidden" value="<?= $cpzone; ?>">
                                    <input name="logout" class="btn btn-info" type="submit" value="DECONNEXION">
                                </form class=form>
                                <table class="table">
                                    <tbody style="background-color: rgba(241, 235, 235, 0.285);">
                                        <tr>
                                            <td><span style="font-weight: bold; ">Identifiant</span>
                                                <br><?= $username; ?>
                                                <?php if (isset($username) && (strpos($username, "omnis_") !== true)): ?>
                                                    <a href="http://192.168.11.150:8080/user/edit_pwd/<?= $sessionid ?>">
                                                        <img width="25" height="25" class="edit" src="https://img.icons8.com/cotton/64/create-new--v5.png" alt="create-new--v5" style="position: relative;; height: 25px;float: right ;display: inline;border-radius: 3px;" />
                                                    </a>
                                                <?php endif;?>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td><span style="font-weight: bold;">Profil</span><br>
                                                <?php for ($i = 0; $i < count($user_profils); $i++) : ?>
                                                    <?= $user_profils[$i] . ' ' ?>
                                                <?php endfor ?>
                                                <?php if (count($user_profils) == 0) : ?>
                                                    <?= "Néant" ?>
                                                <?php endif ?>
                                            </td>
                                        </tr>
                                        <tr>
                                            <td><span style="font-weight: bold;">Service</span><br>full_access</td>
                                        </tr>
                                        <tr>
                                            <td><span style="font-weight: bold;">Zone d'entrée</span><br>Ambohijatovo</td>
                                        </tr>
                                        <tr>
                                            <td><span style="font-weight: bold;">Plage d'entrée</span><br><?= $plage_entry ?></td>
                                        </tr>
                                        <tr>
                                            <td><span style="font-weight: bold;">Validité</span><br><?= $expiration ?></td>
                                        </tr>
                                        <!-- <tr>
                                            <td><span>Crédit temps</span><br>"credit"</td>
                                        </tr> -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
    <script>
        window.open("<?= $my_redirurl; ?>", "_blank");
    </script>
</body>

</html>