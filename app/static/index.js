$(document).ready(function () {
    // vérifier si l'utilisateur tape le bon format de mot de passe
    // mdp contenant au moins 1 minus, 1 majus, 1 chiffre, 1 caract$ et 8 caractères au total
    const enough_format = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$/;
    const good_format = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+-]).{8,}$/;
    // effacer les bordures des input
    $('.inputBox>input').addClass('without_border');

    // ajouter un avertissement imaginaire de id='advert' en bas de l'input #newPassd, masquer par défaut
    $(".inputBox:has('#newPassd')").append("\
        <div id='advert'>\
            <p class='poor_pwd' style=>Faible</p>\
            <p class='enough_pwd'>Assez-bon</p>\
            <p class='good_pwd'>Bon</p>\
        </div>")
    $('#advert').hide();
    $('#advert').children().css("display", "none");


    $('#newPassd').on("keyup", function () {
        var passd = $(this).val();
        $('#advert').show();
        $(this).removeClass('without_border');
        if(passd.length < 4){
            $(this).addClass("poor_pwd").removeClass("enough_pwd").removeClass("good_pwd")
            $('.poor_pwd').fadeIn("fast");
            $("p[class!='poor_pwd']").hide();
        }
        else if(passd.length < 8){
            $(this).addClass("enough_pwd").removeClass("poor_pwd").removeClass("good_pwd");
            $('.enough_pwd').fadeIn("fast");
            $("p[class!='enough_pwd']").hide();
            
        }
        else if(good_format.test(passd)){
            $(this).addClass("good_pwd").removeClass("poor_pwd").removeClass("enough_pwd")
            $('.good_pwd').fadeIn("fast");
            $("p[class!='good_pwd']").hide();
        }
        
    });

    // // Vériifier si les deux mots de passe sont identiques
    // $('#cnfPassd').on("keyup", function () {
    //     $('#advert').fadeOut("slow");
    //     if($(this).val() != $('#newPassd').val()){
    //         $(this).addClass('poor_pwd');
    //     }
        
    // });
});