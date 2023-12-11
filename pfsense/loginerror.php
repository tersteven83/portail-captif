<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="captiveportal-login.css">
    <title>Document</title>
    <style>
 

body {
  font-family: sans-serif;
  font-size: 16px;
}

.login {
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
}

.login-space {
  width: 100%;
  padding: 0;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.group {
  margin-bottom: 10px;
}

.label {
  font-size: 14px;
  margin-bottom: 5px;
}

.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
}

.button {
  background-color: #000;
  color: #fff;
  padding: 10px;
  border: none;
  cursor: pointer;
}

@media (max-width: 300px) {
  .login-space {
    margin-top: 20px;
  }
  .login-form {
    width: 300px;
  }

  .label {
    font-size: 12px;
    margin-bottom: 5px;
  }

  .input {
    width: 100%;
    padding: 5px;
    border: 1px solid #ccc;
  }

  .button {
    font-size: 10px;
    padding: 5px;
    margin-right: auto;
  }
}


    </style>
</head>
<body>

    <form method="POST" action="$PORTAL_ACTION$">

    <div class ="row">
        <div class="col-md-6 mx-auto p-0">
            <div class="card">
    <div class="login-box">
        <div class="login-snip">

            <div>
                <img src="captiveportal-logo-omnis.png" alt="logo-omnis" style=" max-width: 80px;min-width: 70; margin-left: 5%;align-items: center;">
            </div>


            <div class="check">
            
            <?php if (isset($PORTAL_MESSAGE)):?>
            <p style="font-weight: normal; color: red;padding-left: 15px; "><?=$PORTAL_MESSAGE;?></p>
            <?php endif;?>
            

            <input id="tab-1" type="radio" name="tab" class="sign-in" checked><label for="tab-1" class="tab" style="padding-left: 15px;">Login</label>
            <input id="tab-2" type="radio" name="tab" class="sign-up"><label for="tab-2" class="tab"  style="padding-left: 10px;">à propos</label>
         
            <div class="login-space" " >
                <div class="login">
                    <div class="group" style="padding-left: 15px;">
                        <label for="auth_user" class="label" style="display: block; padding-left: 5px;">Username</label>
                        <input id="user" name="auth_user" type="text" class="input"  placeholder="Enter your username" style="width: 80%;">
                    </div>
                    <div class="group" style="padding-left: 15px;">
                        <label for="auth_pass" class="label">Password</label >
                        <input id="pass" name="auth_pass" type="password" class="input" data-type="password" placeholder="Enter your password" style="width: 80%" >
                        <input type="hidden" value="$PORTAL_ZONE$">
                    </div>
        
            
                    <!--<div class="group">
                        <input id="check" type="checkbox" class="check" checked>
                        <label for="check"><span class="icon"></span> Keep me Signed in</label>
                    </div>-->
                    <div class="group" style="margin-top: 10%; padding-left: 15px; margin-right: auto;">
                        <input type="submit" class="button" value="login" name="accept" style="max-width: 80%;  max-height: 30px; font-size: 10px; padding-top:6px; padding-left: 15px; ">
                        <a href="http://192.168.11.150:8080/auth/gather_id" style="font-weight: normal; margin-left: 22%;">mot de passe oublié?</a>
                    </div>

                    <div class="sign-up-form" style="padding-left: 20px;">
                        <p>
                            Bienvenue cher utilisateur,veuillez vous identifier à fin de savoir votre identité pour votre connexion .
                          
                            
                        </p>
                    
                </div>  
                 
                </div>
                    <div class="sign-up-form">
                        <p>
                            Bienvenue cher utilisateur,veuillez vous identifier à fin de savoir votre identité pour votre connexion .
                          
                        </p>
                    
                    </div>
            </div>
        </div>
    </div>   

    </form>

    
</body>
</html>