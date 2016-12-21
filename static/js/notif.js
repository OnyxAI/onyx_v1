(function($){

	$.notif = function(options){


		$("body").notif(options)

	};

	$.fn.notif = function(options){

		var settings = {	//Est un tableau contenant le code de la notif

		html:'<div class="notification animated fadeInLeft {{cls}}">          <div class="gauche">          	{{#icon}}            <div class="icone">              {{{icon}}}            </div>            {{/icon}}            {{#img}}            <div class="img" style="background-image:url({{img}});"></div>            {{/img}}          </div>          <div class="droite">            <h2>{{title}}</h2>            <p>{{content}}</p>          </div>        </div>',
		
		icon:"&#8505;", // L'icon par défaut est celui la ( icon sur http://www.entypo.com/characters/)
		timeout:3e3}; // Voit si il y a un timeout qui enleve la notif

		if(options.cls == "error"){	//Si la class est égale à error alors on met l'icon error

			settings.icon = "&#10060;"

		}if(options.cls == "success"){ //Si la class est égale à success alors on met l'icon success

			settings.icon = "&#10003;"

		}

		var options = $.extend(settings , options); // Créer une variable contenant le body à utiliser



		return this.each(function(){ // Renvoie cette fonction
			var settings = $(this); // Pour simplifier le nom de la variable on la renomme simplement
			var $notif = $("> .notifications" , this); // Recherche si il y a .notifications
			var $notifs = $(Mustache.render(options.html , options)); // On appel notif quand on rend une notif avec un effet créer par Mustache
			if($notif.length == 0){	//Si c'est la premiere notification alors on on met l'effet flipInX
				$notif = $('<div class="notifications animated flipInX"/>'
					);
				settings.append($notif)
			}
			$notif.append($notifs);
			if(options.timeout){	//Si il y a un timeout alors on ajoute un timeout a la notif
				setTimeout(function(){
					$notifs.trigger("click")
				},options.timeout)

			}

			$notifs.click(function($){	// Si on click sur une notif alors elle s'éfface

				$.preventDefault();
				$notifs.addClass("zoomOutUp").delay(500).slideUp(300,function(){

					if($notifs.siblings().length == 0){

						$notif.remove()
					}
					$notifs.remove()

				})
			})
		})
	};

	$("#notif").click(function(options){	//On recupere les informations concernant la notif à afficher
			options.preventDefault();
			$.notif($(this).data())
	})


})(jQuery)